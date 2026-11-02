-- Read-only PDF navigation inspector for the assembled course.
-- Usage: texlua scripts/inspect_book_pdf.lua input.pdf output.json
-- Requires only the libraries shipped with texlua (pdfe, utf8, lfs).
-- pdfe API: LuaTeX Reference Manual, sections14.2.5--14.2.11:
-- https://texdoc.org/serve/luatex/0 (printed pp.292--295).
-- Exit0: complete inspection without structural errors/unresolved local targets.
-- Exit1: JSON written, but inspection found errors; exit2: CLI/output failure.

local input, output = arg[1], arg[2]
if not input or not output or arg[3] then
  io.stderr:write("Usage: texlua scripts/inspect_book_pdf.lua input.pdf output.json\n")
  os.exit(2)
end
local function absolute(path)
  path = path:gsub("\\", "/")
  if not path:match("^%a:/") and path:sub(1,1) ~= "/" then path = lfs.currentdir():gsub("\\", "/") .. "/" .. path end
  local parts = {}
  for part in path:gmatch("[^/]+") do
    if part == ".." then table.remove(parts) elseif part ~= "." then parts[#parts+1] = part end
  end
  return (path:sub(1,1) == "/" and "/" or "") .. table.concat(parts, "/"):lower()
end
if not output:lower():match("%.json$") or absolute(input) == absolute(output) then
  io.stderr:write("Output must be a distinct .json file; the PDF is never overwritten.\n")
  os.exit(2)
end

local array_mt, null = {}, {}
local function array(t) return setmetatable(t or {}, array_mt) end
local function nullable(v) if v == nil then return null else return v end end
local function escape(s)
  return '"' .. s:gsub('[%z\1-\31\\"]', function(c)
    local map = {['"']='\\"', ['\\']='\\\\', ['\n']='\\n', ['\r']='\\r', ['\t']='\\t'}
    return map[c] or string.format("\\u%04x", c:byte())
  end) .. '"'
end
local function json(v, indent)
  indent = indent or ""
  if v == null or v == nil then return "null" end
  if type(v) == "string" then return escape(v) end
  if type(v) == "boolean" then return tostring(v) end
  if type(v) == "number" then
    if v ~= v or v == math.huge or v == -math.huge then return "null" end
    return string.format("%.14g", v)
  end
  assert(type(v) == "table", "Unexpected JSON value: " .. type(v))
  local is_array, items = getmetatable(v) == array_mt, {}
  if is_array then
    for i=1,#v do items[#items+1] = json(v[i], indent .. "  ") end
  else
    local keys = {}; for k in pairs(v) do keys[#keys+1] = k end; table.sort(keys)
    for _,k in ipairs(keys) do items[#items+1] = escape(k) .. ": " .. json(v[k], indent .. "  ") end
  end
  local left, right = is_array and "[" or "{", is_array and "]" or "}"
  if #items == 0 then return left .. right end
  return left .. "\n" .. indent .. "  " .. table.concat(items, ",\n" .. indent .. "  ") .. "\n" .. indent .. right
end

local report = {
  schema_version=1, input_pdf=input, status="inspecting", page_count=0,
  coordinates="PDF default user space; origin and rotation are retained in each page record. Physical pages are one-based; PDF number-tree indices are zero-based.",
  pages=array(), named_destinations=array(), internal_links=array(), other_links=array(),
  outlines=array(), page_labels={present=false, ranges=array(), labels=array()},
  unresolved_internal_targets=array(), errors=array(), warnings=array(),
}
local function issue(kind, message, context)
  report[kind][#report[kind]+1] = {message=message, context=context or {}}
end
local function error_at(message, context) issue("errors", message, context) end
local function warning(message, context) issue("warnings", message, context) end

-- PDF text strings default to PDFDocEncoding, not Latin-1. Names may be UTF-8.
local pdfdoc = {
  [0x18]=0x02D8,[0x19]=0x02C7,[0x1A]=0x02C6,[0x1B]=0x02D9,[0x1C]=0x02DD,[0x1D]=0x02DB,[0x1E]=0x02DA,[0x1F]=0x02DC,
  [0x7F]=0xFFFD,[0x80]=0x2022,[0x81]=0x2020,[0x82]=0x2021,[0x83]=0x2026,[0x84]=0x2014,[0x85]=0x2013,[0x86]=0x0192,[0x87]=0x2044,
  [0x88]=0x2039,[0x89]=0x203A,[0x8A]=0x2212,[0x8B]=0x2030,[0x8C]=0x201E,[0x8D]=0x201C,[0x8E]=0x201D,[0x8F]=0x2018,
  [0x90]=0x2019,[0x91]=0x201A,[0x92]=0x2122,[0x93]=0xFB01,[0x94]=0xFB02,[0x95]=0x0141,[0x96]=0x0152,[0x97]=0x0160,
  [0x98]=0x0178,[0x99]=0x017D,[0x9A]=0x0131,[0x9B]=0x0142,[0x9C]=0x0153,[0x9D]=0x0161,[0x9E]=0x017E,[0x9F]=0xFFFD,[0xA0]=0x20AC,[0xAD]=0xFFFD,
}
local function text_string(s, name)
  if type(s) ~= "string" then return nil end
  local bom = s:sub(1,2)
  if bom == "\254\255" or bom == "\255\254" then
    local little, out, i = bom == "\255\254", {}, 3
    local function word(pos)
      local a,b=s:byte(pos,pos+1); if not b then return nil end
      return little and b*256+a or a*256+b
    end
    while i<=#s do
      local code=word(i); i=i+2
      if not code then code=0xFFFD
      elseif code>=0xD800 and code<=0xDBFF then
        local low=word(i)
        if low and low>=0xDC00 and low<=0xDFFF then code=0x10000+(code-0xD800)*1024+low-0xDC00; i=i+2 else code=0xFFFD end
      elseif code>=0xDC00 and code<=0xDFFF then code=0xFFFD end
      out[#out+1]=utf8.char(code)
    end
    return table.concat(out)
  end
  if s:sub(1,3)=="\239\187\191" then s=s:sub(4); name=true end
  if name and utf8.len(s) then return s end
  local out={}; for i=1,#s do local b=s:byte(i); out[#out+1]=utf8.char(pdfdoc[b] or b) end
  return table.concat(out)
end
local function kind(v)
  if type(v)=="userdata" then return pdfe.type(v) end
  return type(v)
end
local function isdict(v) return kind(v)=="pdfe.dictionary" end
local function isarray(v) return kind(v)=="pdfe.array" end
local function raw_member(parent, key)
  if isarray(parent) then return pdfe.getfromarray(parent,key) end
  if isdict(parent) then
    for i=1,#parent do
      local k,t,v,d=pdfe.getfromdictionary(parent,i)
      if k==key then return t,v,d end
    end
  end
end
local function member(parent,key)
  if not isdict(parent) and not isarray(parent) then return nil end
  local t=raw_member(parent,key)
  -- In the installed API, typed array getters use zero-based indices, unlike
  -- Lua [i] access and getfromarray, which both use one-based indices.
  local typed_key=isarray(parent) and key-1 or key
  if t==6 then return pdfe.getstring(parent,typed_key,true) end
  if t==5 then return pdfe.getname(parent,typed_key) end
  local value=parent[key]
  if type(value)=="string" then return pdfe.getstring(parent,typed_key,true) or pdfe.getname(parent,typed_key) or value end
  return value
end
local function object_number(parent,key)
  local t,v,detail=raw_member(parent,key)
  if t==10 then return type(detail)=="number" and detail or type(v)=="number" and v or nil end
end
local function object_key(value,parent,key)
  local n=parent and object_number(parent,key)
  return n and "object:"..n or tostring(value)
end
local function numbers(value)
  local out=array()
  if value and (isarray(value) or type(value)=="table") then
    for i=1,#value do local n=value[i]; out[#out+1]=type(n)=="number" and n or null end
  end
  return out
end
local function inherited(page,key)
  local node,depth=page,0
  while isdict(node) and depth<64 do
    local value=member(node,key); if value~=nil then return value end
    node=member(node,"Parent"); depth=depth+1
  end
end

local doc, page_objects, page_dictionaries, named = nil, {}, {}, {}
local function resolve(value, stack, depth)
  stack,depth=stack or {},depth or 0
  if depth>64 then return {kind="invalid", error="Destination nesting exceeds64 levels"} end
  if type(value)=="string" then
    local result={kind="named", name=text_string(value,true)}
    if stack[value] then result.error="Cyclic named destination"; return result end
    if not named[value] then result.error="Named destination is absent"; return result end
    stack[value]=true
    local target=resolve(named[value].value,stack,depth+1)
    stack[value]=nil
    result.resolved_page=target.resolved_page; result.coordinates=target.coordinates
    result.fit=target.fit; result.page_object_number=target.page_object_number
    result.error=target.error
    return result
  end
  if isdict(value) then return resolve(member(value,"D"),stack,depth+1) end
  if not isarray(value) then return {kind="invalid", error="Destination is not an array, name, string or destination dictionary"} end
  local target={kind="explicit", coordinates={}, parameters=array()}
  local t,v,d=raw_member(value,1)
  if t==10 then
    target.page_object_number=type(d)=="number" and d or type(v)=="number" and v or nil
    target.resolved_page=page_objects[target.page_object_number]
  elseif t==8 then target.resolved_page=page_dictionaries[tostring(v)]
  elseif t==3 then
    target.error="Integer page target is not a local PDF page-object reference"
    target.page_index_zero_based=v
  end
  target.fit=text_string(member(value,2),true)
  for i=3,#value do target.parameters[#target.parameters+1]=nullable(member(value,i)) end
  local p=target.parameters
  if target.fit=="XYZ" then target.coordinates={left=p[1] or null,top=p[2] or null,zoom=p[3] or null}
  elseif target.fit=="FitH" or target.fit=="FitBH" then target.coordinates={top=p[1] or null}
  elseif target.fit=="FitV" or target.fit=="FitBV" then target.coordinates={left=p[1] or null}
  elseif target.fit=="FitR" then target.coordinates={left=p[1] or null,bottom=p[2] or null,right=p[3] or null,top=p[4] or null}
  elseif target.fit~="Fit" and target.fit~="FitB" then target.error="Unknown or missing destination fit mode" end
  if not target.resolved_page and not target.error then target.error="Destination page object is absent from the page tree" end
  return target
end
local function checked_target(value,context)
  local target=resolve(value)
  if target.error then
    report.unresolved_internal_targets[#report.unresolved_internal_targets+1]={context=context,target=target,reason=target.error}
  end
  return target
end
local function action_target(owner,context)
  local dest=member(owner,"Dest")
  if dest~=nil then return checked_target(dest,context),true end
  local a=member(owner,"A")
  if not isdict(a) then return nil,false end
  local action=member(a,"S")
  if action=="GoTo" then return checked_target(member(a,"D"),context),true end
  if action=="Named" then
    local n=member(a,"N")
    local page=({FirstPage=1,LastPage=report.page_count,NextPage=(context.source_page or 0)+1,PrevPage=(context.source_page or 0)-1})[n]
    if page and page>=1 and page<=report.page_count then return {kind="named_action",action=n,resolved_page=page},true end
    warning("Named action cannot be resolved as local page navigation",context)
  end
  return {kind="nonlocal_action",action=nullable(text_string(action,true)),uri=nullable(text_string(member(a,"URI"),true))},false
end

local function add_name(name,value,origin)
  if type(name)~="string" then error_at("Invalid named-destination key",{origin=origin}); return end
  if named[name] then error_at("Duplicate named destination",{name=text_string(name,true),first=named[name].origin,second=origin}); return end
  named[name]={value=value,origin=origin}
end
local function name_tree(node,seen,depth)
  if not isdict(node) then error_at("Invalid destination name-tree node"); return end
  if depth>64 then error_at("Destination name tree exceeds64 levels"); return end
  local key=tostring(node); if seen[key] then error_at("Repeated/cyclic destination name-tree node"); return end; seen[key]=true
  local entries,kids=member(node,"Names"),member(node,"Kids")
  if entries then
    if not isarray(entries) then error_at("Name-tree Names is not an array"); return end
    if #entries%2~=0 then error_at("Odd number of destination name-tree entries") end
    for i=1,#entries-1,2 do add_name(member(entries,i),member(entries,i+1),"Names.Dests") end
  end
  if kids then
    if not isarray(kids) then error_at("Name-tree Kids is not an array"); return end
    for i=1,#kids do name_tree(member(kids,i),seen,depth+1) end
  end
end

local outline_seen,outline_count={},0
local function outline_chain(first,parent,key,depth)
  local result=array(); local node,owner,field=first,parent,key
  if depth>64 then error_at("Outline hierarchy exceeds64 levels"); return result end
  while node do
    if not isdict(node) then error_at("Outline item is not a dictionary"); break end
    local id=object_key(node,owner,field)
    if outline_seen[id] then error_at("Repeated/cyclic outline item",{object=id}); break end
    outline_seen[id]=true; outline_count=outline_count+1
    local title=text_string(member(node,"Title"))
    local context={kind="outline",ordinal=outline_count,title=nullable(title)}
    local target,internal=action_target(node,context)
    local item={ordinal=outline_count,title=nullable(title),depth=depth,
      object_number=nullable(object_number(owner,field)),target=nullable(target),internal=internal,
      resolved_page=target and nullable(target.resolved_page) or null,
      count=nullable(member(node,"Count")),children=array()}
    local child=member(node,"First")
    if child then item.children=outline_chain(child,node,"First",depth+1) end
    result[#result+1]=item; owner,field=node,"Next"; node=member(node,"Next")
  end
  return result
end

local function roman(n)
  local result={}; local vals={{1000,"M"},{900,"CM"},{500,"D"},{400,"CD"},{100,"C"},{90,"XC"},{50,"L"},{40,"XL"},{10,"X"},{9,"IX"},{5,"V"},{4,"IV"},{1,"I"}}
  for _,pair in ipairs(vals) do while n>=pair[1] do result[#result+1]=pair[2]; n=n-pair[1] end end
  return table.concat(result)
end
local function label_text(range,physical)
  local n=range.start_number+physical-range.start_page
  local suffix=""; local style=range.style
  if style=="D" then suffix=tostring(n)
  elseif style=="R" or style=="r" then suffix=roman(n); if style=="r" then suffix=suffix:lower() end
  elseif style=="A" or style=="a" then suffix=string.rep(string.char((style=="A" and 65 or 97)+(n-1)%26),math.floor((n-1)/26)+1)
  elseif style~=null then return nil end
  return range.prefix..suffix
end
local function labels_tree(node,seen,depth)
  if not isdict(node) then error_at("Invalid PageLabels number-tree node"); return end
  if depth>64 then error_at("PageLabels number tree exceeds64 levels"); return end
  local id=tostring(node); if seen[id] then error_at("Repeated/cyclic PageLabels node"); return end; seen[id]=true
  local nums,kids=member(node,"Nums"),member(node,"Kids")
  if nums then
    if not isarray(nums) then error_at("PageLabels Nums is not an array"); return end
    if #nums%2~=0 then error_at("Odd number of PageLabels number-tree entries") end
    for i=1,#nums-1,2 do
      local start,definition=member(nums,i),member(nums,i+1)
      if type(start)~="number" or start%1~=0 or start<0 or start>=report.page_count or not isdict(definition) then
        error_at("Invalid PageLabels range")
      else
        local number=member(definition,"St") or 1
        if type(number)~="number" or number<1 or number%1~=0 then error_at("Invalid PageLabels St value"); number=1 end
        report.page_labels.ranges[#report.page_labels.ranges+1]={start_page_zero_based=start,start_page=start+1,
          style=nullable(member(definition,"S")),prefix=text_string(member(definition,"P")) or "",start_number=number}
      end
    end
  end
  if kids then
    if not isarray(kids) then error_at("PageLabels Kids is not an array"); return end
    for i=1,#kids do labels_tree(member(kids,i),seen,depth+1) end
  end
end

local ok,fatal=pcall(function()
  doc=assert(pdfe.open(input),"Cannot open PDF")
  report.file_bytes=pdfe.getsize(doc)
  local catalog=assert(pdfe.getcatalog(doc),"PDF has no catalog")
  local pages=pdfe.pagestotable(doc)
  report.page_count=pdfe.getnofpages(doc)
  if #pages~=report.page_count then error_at("Page-tree enumeration disagrees with PDF page count") end
  for i,entry in ipairs(pages) do
    page_objects[entry[3]]=i; page_dictionaries[tostring(entry[1])]=i
    local media=numbers(pdfe.getbox(entry[1],"MediaBox"))
    local crop=numbers(pdfe.getbox(entry[1],"CropBox")); if #crop==0 then crop=media end
    local unit=member(entry[1],"UserUnit") or 1
    local dimensions={}
    if #media==4 and type(media[1])=="number" and type(media[4])=="number" then
      dimensions={width_pt=(media[3]-media[1])*unit,height_pt=(media[4]-media[2])*unit}
    else error_at("Page lacks a valid MediaBox",{source_page=i}) end
    report.pages[#report.pages+1]={physical_page=i,object_number=entry[3],media_box=media,crop_box=crop,
      dimensions=dimensions,rotation=inherited(entry[1],"Rotate") or 0,user_unit=unit,annotation_count=0,internal_link_count=0}
  end

  local names=member(catalog,"Names")
  if isdict(names) and member(names,"Dests") then name_tree(member(names,"Dests"),{},0) end
  local old=member(catalog,"Dests")
  if old then
    if not isdict(old) then error_at("Catalog Dests is not a dictionary")
    else for i=1,#old do local key=pdfe.getfromdictionary(old,i); add_name(key,member(old,key),"Catalog.Dests") end end
  end
  local keys={}; for name in pairs(named) do keys[#keys+1]=name end; table.sort(keys)
  for _,name in ipairs(keys) do
    local target=checked_target(named[name].value,{kind="named_destination",name=text_string(name,true)})
    report.named_destinations[#report.named_destinations+1]={name=text_string(name,true),origin=named[name].origin,
      target=target,resolved_page=nullable(target.resolved_page),coordinates=target.coordinates or {}}
  end

  for i,entry in ipairs(pages) do
    local annots=member(entry[1],"Annots")
    if annots then
      if not isarray(annots) then error_at("Page Annots is not an array",{source_page=i})
      else
        report.pages[i].annotation_count=#annots
        for j=1,#annots do
          local annot=member(annots,j)
          if isdict(annot) and member(annot,"Subtype")=="Link" then
            local context={kind="link",source_page=i,annotation_index=j}
            local target,internal=action_target(annot,context)
            local link={source_page=i,annotation_index=j,object_number=nullable(object_number(annots,j)),
              rect=numbers(member(annot,"Rect")),destination=nullable(target),resolved_page=target and nullable(target.resolved_page) or null}
            if internal then report.internal_links[#report.internal_links+1]=link; report.pages[i].internal_link_count=report.pages[i].internal_link_count+1
            else report.other_links[#report.other_links+1]=link end
          end
        end
      end
    end
  end

  local outlines=member(catalog,"Outlines")
  if outlines then
    if not isdict(outlines) then error_at("Catalog Outlines is not a dictionary")
    else report.outlines=outline_chain(member(outlines,"First"),outlines,"First",0) end
  end
  local labels=member(catalog,"PageLabels")
  if labels then report.page_labels.present=true; labels_tree(labels,{},0) end
  table.sort(report.page_labels.ranges,function(a,b) return a.start_page<b.start_page end)
  local ranges=report.page_labels.ranges
  for i=2,#ranges do if ranges[i].start_page==ranges[i-1].start_page then error_at("Duplicate PageLabels range start",{page=ranges[i].start_page}) end end
  if labels and (#ranges==0 or ranges[1].start_page~=1) then error_at("PageLabels does not start at physical page1") end
  local range_index=1
  for i=1,report.page_count do
    while ranges[range_index+1] and ranges[range_index+1].start_page<=i do range_index=range_index+1 end
    local label=tostring(i)
    if ranges[range_index] and ranges[range_index].start_page<=i then
      label=label_text(ranges[range_index],i)
      if not label then error_at("Unknown PageLabels style",{source_page=i}); label=tostring(i) end
    end
    report.page_labels.labels[#report.page_labels.labels+1]=label
    if report.pages[i] then report.pages[i].label=label end
  end
  report.counts={named_destinations=#report.named_destinations,internal_links=#report.internal_links,
    other_links=#report.other_links,outline_items=outline_count,page_label_ranges=#ranges}
end)
if not ok then error_at("Inspector failed: "..text_string(tostring(fatal),true)) end
if doc then pdfe.close(doc) end
report.status=(#report.errors==0 and #report.unresolved_internal_targets==0) and "passed" or "failed"
local written,write_error=pcall(function()
  local handle=assert(io.open(output,"wb")); handle:write(json(report).."\n"); assert(handle:close())
end)
if not written then io.stderr:write("Cannot write inspection JSON: "..tostring(write_error).."\n"); os.exit(2) end
io.stdout:write(string.format("%s: %d pages, %d destinations, %d internal links, %d outlines; %d errors, %d unresolved targets\n",
  report.status,report.page_count,#report.named_destinations,#report.internal_links,outline_count,#report.errors,#report.unresolved_internal_targets))
os.exit(report.status=="passed" and 0 or 1)
