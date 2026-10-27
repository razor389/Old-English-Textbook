"""Repair initial compositions transparently; preserve the initial witness."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[3]; O=Path(__file__).resolve().parent
D=json.loads((O/'initial-independent-models.json').read_text(encoding='utf-8'))
P={p['source_item_id']:p for p in json.loads((R/'sources/audits/unit16-source/exercises-prompts.json').read_text(encoding='utf-8'))['items']}
repairs=[]
def change(item,new,reason,refs):
    row=next(r for r in D['items'] if r['source_item_id'].endswith(item))
    old=row['model']
    if old!=new:
        repairs.append({'amendment_id':f'U16-G-M{len(repairs)+1:02d}','source_item_id':row['source_item_id'],'initial_model':old,'replacement_model':new,'reason':reason,'evidence_refs':refs})
    row['model']=new
    row['source_prompt']=P[row['source_item_id']]['prompt']
change('32-03','Hē ārās and bebēad ðǣm winde, and cwæð tō ðǣre sǣ, Geswīc.','Use the independently attested ordinary cease verb and its complete newly taught command pair; initial Gestille was not a selected imperative.',['U16-G-BT-GESWICAN','U16-G-FB54'])
change('32-05','Ðū hīerst his stefne, and ðū ne wāst hwanon hē cymð, ne hwider hē gǣð.','Replace the unsupported initial contracted form with the selected prior uncontracted witan form and ne. No negative-witan paradigm is silently imported.',['U16-G-FB76','U16-G-FB76'])
change('32-06','Hē geseah twēgen brōðor hiera nętt on ðā sǣ sęndan; hīe wǣron fisceras.','Cook source nętt has hooked ę. Retain its singular accusative.',['U16-EX-P18','U16-EX-P19'])
change('32-07','And hē sægde him, Cumað æfter mē, and ic dō ðæt git bēoð manna fisceras; and hīe sōna forlēt-on hiera nętt.'.replace('forlēt-on','forlēton'),'BT208b directly attests dō + ðæt git bēoð manna fisceras with dual subject and future-context indicative plural. Heavy neuter nętt has zero nominative/accusative plural; remove initial temporary word-division placeholder.',['U16-G-BT-DON','U16-G-WRIGHT174','U16-G-WRIGHT175'])
change('32-11','Ðonne hē hām cymð, hē cleopað his frīend and his nēahgebūras tōgædere and cwið, Blissiað mid mē, for-ðon-ðe ic mīn forloren scēap fand.','Select strong neuter accusative singular forloren after possessive mīn; first-person singular findan uses the actual prior selected fand, not its third-singular variant funde.',['U16-G-FB60','U16-G-FB61','U16-G-FB100'])
change('33-01','And, intō ðǣm hūse gangende, hīe fundon ðæt bearn mid Marian his mēder.','Use previously productive bearn and the prior selected dative article; gangan participial expression remains locally supplied.',['U16-EX-P19'])
change('33-02','Ārīs, and nim ðæt bearn and his mōdor on niht, and flēoh tō Egypta lande, and bēo ðǣr oð ðæt ic ðē sęcge.','Use productive bearn; retain every clause and until-verb-final control.',['U16-EX-P19'])
change('33-03','Hē ðā ārās and nam ðæt bearn and his mōdor on niht and fērde on Egypta land, ðæt gefylled wǣre ðæt fram Drihtne ðurh ðone wītgan cweden wæs, Of Egyptum ic mīnne sunu cleopode.','Use productive bearn. Passive purpose, quoted simple preterite and all explicit omissions remain.',['U16-EX-P19','U16-EX-P20'])
change('34-02','Gif ðū nānne ne finde ðe ðē fēde, ęfthweorf hider.','Use the previously assigned return lexeme with a complete newly taught command pair instead of accidentally importing a supplied-only unprefixed węndan sense.',['U16-G-FB105','U16-G-FB167'])
change('34-03','Genyhtsumien mīne bēc unc bǣm.','The high-resolution source says books; the initial source-editor hooks reading was a transcription error, not a Cook error. Use the explicitly cited p167 genyhtsumien construction with the requested books substituted.',['U16-EX-P20','U16-G-FB167'])
change('34-06','Ic hālsie ðē ðurh ðone libbendan God ðæt ðū ūs sęcge gif ðū sīe Crīst, Godes Sunu.','Preserve the actual selected hālsie and Crīst quantities; the newly assigned oath frame has an accusative person and ðurh standard.',['U16-G-FB297','U16-EX-P20'])
change('34-10','Ðonne Crīst cymð, ðonne ne wāt nān mann hwanon hē is.','Use existing uncontracted wāt with negative concord; avoid an unassigned nytan paradigm.',['U16-G-FB76'])
change('35-03','Gā ðæs weges ðe ðū cōme.','The explicit genitive route is attested in Cook169.16–17 and §157. The initial accusative alternative is withdrawn from the selected model pending separate evidence.',['U16-G-FB169','U16-G-FB92'])
change('35-04','Ic ne plegode nǣfre bęt ðonne ic tō-dæg dyde.','Use the selected prior comparative adverb bęt. Teach action comparison and substitute-action dōn explicitly.',['U16-G-FB170','U16-G-BT-DON'])
change('35-05','Hēo ne sang nǣfre bęt ðonne hēo nū dyde.','Use selected bęt and retain narrated now. Comparative action clause and substitute do are explicitly newly taught.',['U16-G-FB170','U16-G-BT-DON'])
change('35-10','Ðā hē ðǣre burge geate nēalǣcte, ðā wæs ðǣr dēad mann boren.','Preserve actual previously taught nēalǣcte rather than introduce an unassigned -hte variant. The source hint is then ðā, not a gān verb.',['U16-EX-P21','U16-G-FB94'])
change('35-11','Ic gesēo mǣden geond ðā strǣt iernan.','Cook selects mǣden without g; source168.4–5 directly supports geond + street accusative and perception iernan.',['U16-G-FB168','U16-G-EX49'])
change('36-02','Ðā bewęnde hē him tō ðǣm wīfe and cwæð, Gesihst ðū ðis wīf? Ic ēode intō ðīnum hūse; ðū ne sealdest mē wæter tō mīnum fōtum; ðēos ðwōh mīne fēt mid hiere tēarum.','Cook explicitly points to §184a dative reflexive: use him. Feminine ðēos resumes the female person; it is a bounded semantic-reference choice, not the neuter noun’s grammatical gender.',['U16-G-FB100','U16-EX-P22'])
change('36-04','Mīn hēafod ðū mid ęlum ne smiredest; ðēos smirede mīne fēt mid sealfe.','Correct second-singular weak past ending -st. Retain plural oils as instructed and singular ointment.',['U16-G-FB68','U16-G-FB69','U16-EX-P22'])
change('32-08','Gif ðīn hand oððe ðīn fōt ðē ǣswicað, āceorf hit of, and weorp fram ðē; betere ðē is ðæt ðū healt on līf gā, ðonne ðū twā handa and twēgen fēt hæbbe and on ēce fȳr sīe worpen.','Use the actual prior selected past participle worpen, not an unassigned prefixed spelling. The mixed alternative hand/foot is resumed by generic neuter hit.',['U16-G-FB61','U16-PRIOR-WEORPAN'])
change('33-09','Hē sægde him, Ic wille gān on fiscnoð; hīe sægdon, And wē willað gān mid ðē.','Use the personally verified Cook167 spelling fiscnoð in the exact fishing phrase.',['U16-G-FB167'])
change('34-08','Sīe inc bǣm æfter incrum gelēafan.','Use the selected bǣm both form consistent with Cook167 and the newly taught bēgen table.',['U16-G-FB167'])
change('34-07','Ic ēow sęcge, Æfter ðissum gē gesēoð Mannes Sunu on ðā swīðran hand Godes mægenðrymmes sittan and on heofones wolcnum cuman.','Use the two actual productive plain infinitives sittan and cuman in the prior perception construction, with shared accusative actor Sunu. The initial participial spellings lacked explicit agreement/status support. Every English action and prepositional control remains.',['U16-G-FB96','U16-PRIOR-PERCEPTION','U16-EX-P20'])
change('34-13','Gif ic mē selfne wuldrie, nis mīn wuldor nāwiht; mīn Fæder is sē ðe mē wuldrað, be ðǣm gē cweðað ðæt hē ēower God sīe.','Use the explicitly selected weak-II first-singular -ie series; the g spelling remains a documented variant rather than an unnoticed new cell.',['U16-G-FB73','U16-G-FB74'])
change('35-12','Smiere mē mid ęle.','Select the Cook/Wright ie spelling throughout the smierwan system, explicitly modelled on gierwan. BT smire remains a documented valid variant.',['U16-G-WRIGHT270','U16-G-WRIGHT274','U16-G-BT-SMIRWAN'])
change('35-14','Gif se Sunu ēow ālīest, gē bēoð sōðlice frige.','Cook Exercises48 specifies nominative plural frige. Supply this exact predicate adjective; no whole free-adjective system is inferred.',['U16-EX-P21','U16-G-EX48'])
change('36-03','Ðū mē coss ne sealdest; ðēos, siððan ic inn ēode, ne geswāc ðæt hēo mīne fēt ne cyste.','BT879b quotes Luke7.45 with both matrix and subordinate ne. Supply the entire cessation clause, meaning did not stop kissing; do not invent a general complement rule or read the second ne as a refusal to kiss.',['U16-G-BT-SIDTHAN'])
change('36-04','Mīn hēafod ðū mid ęlum ne smieredest; ðēos smierede mīne fēt mid sealfe.','Retain the corrected second-singular -st and select consistent Cook/Wright ie forms from the explicit smierwan=gierwan model. BT smirede/smyredest are separately documented alternatives.',['U16-G-WRIGHT270','U16-G-WRIGHT271','U16-G-WRIGHT274','U16-G-BT-SMIRWAN'])
change('36-05','For-ðon ic ðē sęcge, Manega synna hiere sindon forgiefen, for-ðon-ðe hēo mē swīðe lufode.','Select uninflected predicative past participle forgiefen, licensed by Cook179. Forgiveness is a newly taught sense; prior give/grant alone did not establish it.',['U16-G-FB100','U16-G-FB288','U16-EX-P22'])
row=next(x for x in D['items'] if x['source_item_id'].endswith('32-08'))
change('32-08',row['model'].replace('betere','bętere'),'Use actual prior god-adjective-comp-nom-n-sg-weak bętere with hooked ę; its weak comparative neuter predicate is selected in the impersonal better construction.',['U16-PRIOR-COMPARATIVE','U16-G-FB95'])
row=next(x for x in D['items'] if x['source_item_id'].endswith('33-03'))
change('33-03',row['model'].replace('nam','nōm').replace('fērde','fōr'),'Use actual productive niman preterite nōm and faran preterite fōr. The unqualified English journeyed does not require a new fēran system, and nam was an unassigned variant.',['U16-PRIOR-NIMAN','U16-PRIOR-FARAN'])
row=next(x for x in D['items'] if x['source_item_id'].endswith('34-09'))
change('34-09',row['model'].replace('cumenne','cumanne'),'Use the actual prior selected cuman-inflected-infinitive cumanne. The source reward hint is separately corrected to āgyldan strongIII; its selected āgylt remains valid and is visibly supplied.',['U16-PRIOR-CUMAN','U16-G-BT-AGYLDAN'])
row=next(x for x in D['items'] if x['source_item_id'].endswith('36-02'))
change('36-02',row['model'].replace('Gesihst','Gesiehst'),'Use the actual prior selected second-singular gesiehst; avoid silently importing a spelling variant.',['U16-PRIOR-GESEON'])
for suffix,repls in [('33-03',{'Drihtne':'dryhtne'}),('33-10',{'nihte':'niht'}),('35-06',{'ðissere':'ðisse'}),('35-10',{'burge':'byrig'}),('36-05',{'Manega':'Maniga'})]:
    row=next(x for x in D['items'] if x['source_item_id'].endswith(suffix))
    s=row['model']
    for a,b in repls.items():s=s.replace(a,b)
    change(suffix,s,'Use the actual prior nominal selected surface verified independently by the source editor; preserve the earlier register identity and milestone.',['U16-PRIOR-NOMINAL-SELECTION'])
for suffix,repls in [('32-02',{'uppan ðǣre sǣ':'uppan ðǣm sǣ'}),('32-03',{'tō ðǣre sǣ':'tō ðǣm sǣ'}),('32-04',{'micel smyltnes':'miclu smyltnes'}),('32-06',{'on ðā sǣ':'on ðone sǣ'}),('34-03',{'mīne bēc':'mīna bēc'}),('35-06',{'on ðisse sǣ':'on ðissum sǣ'}),('35-11',{'ðā strǣt':'ðā strǣte'})]:
    row=next(x for x in D['items'] if x['source_item_id'].endswith(suffix));s=row['model']
    for a,b in repls.items():s=s.replace(a,b)
    change(suffix,s,'Select actual prior morphology/gender: masculine sǣ; feminine miclu; feminine plural mīna; accusative strǣte. These are new-composition repairs, not changes to the original source.',['U16-PRIOR-NOMINAL-SELECTION'])
row=next(x for x in D['items'] if x['source_item_id'].endswith('36-01'))
change('36-01',row['model'].replace('Ne dēmað gē','Ne dēme gē'),'Use the explicitly taught shortened plural command immediately before subject gē, per Cook55§95note. The second command without following subject remains dēmað.',['U16-G-FB55'])
row=next(x for x in D['items'] if x['source_item_id'].endswith('36-03'))
change('36-03',row['model'].replace('inn ēode','inēode'),'Use the actual prior ingān preterite first-singular inēode. This avoids introducing an unsupported separate inn spelling; the independently attested negative cessation clause remains unchanged.',['U16-G-FB168','U16-G-BT-SIDTHAN'])
for row in D['items']:
    new=row['model'].replace('ðām','ðǣm')
    if new!=row['model']:
        repairs.append({'amendment_id':f'U16-G-M{len(repairs)+1:02d}','source_item_id':row['source_item_id'],'initial_model':row['model'],'replacement_model':new,'reason':'Use the actual previously selected ðǣm dative article surface in new composition; original reading spellings remain exact.','evidence_refs':['U16-PRIOR-ARTICLE']})
        row['model']=new
    row['source_prompt']=P[row['source_item_id']]['prompt']
    row['review_status']='revised composition pending final primary/nominal reconciliation'
D['status']='revised_compositions_pending_final_primary_and_nominal_reconciliation'
D['initial_witness']='sources/audits/unit16-grammar/initial-independent-models.json'
D['amendments']='sources/audits/unit16-grammar/model-amendments.json'
(O/'author-only-cook-models.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(O/'model-amendments.json').write_text(json.dumps({'schema_version':1,'initial_witness':D['initial_witness'],'repairs':repairs},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(len(D['items']),'revised models;',len(repairs),'explicit repairs; initial witness unchanged.')
