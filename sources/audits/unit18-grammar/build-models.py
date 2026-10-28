"""Private linguistic hypotheses, never a source transcription or learner key."""
import json
from pathlib import Path
O=Path(__file__).resolve().parent
M={44:[
'Iacob cwæð tō his sunum: Gāð and bycgað ūs sumne dǣl metes.',
'Ðā cwæð Iudas: Ðæs landes ealdor swōr āðas ætforan ūs ðæt wē ne mōsten cuman ætforan hine, būton wē ūrne gingstan brōðor mid ūs bringen.',
'Gif ðū hine mid ūs sęndan wilt, wē gāð ætgædere and bycgað ðā ðing ðe wē beðurfon.',
'Gē ēarmlice wið mē dydon, ðā gē him sægdon ðæt gē mā brōðra hæfden.',
'Se mann āscode ūs hwæðer ūre fæder leofode and hwæðer wē brōðor hæfden, and wē him andswarodon; wē ne wiston ðæt hē wolde giernan ðæt wē ūrne brōðor ðider lǣdden.',
'Iudas cwæð: Sęnd ðone cnapan mid mē, ðæt wē mægen bycgan ðā ðing ðe wē beðurfon, ðæt wē ne forweorðen; būton ic hine hām bringe, sīe ic scyldig.',
'Gif ðēos ęlcung nǣre, wē wǣren ōðre sīð cumen.',
'Ðā cwæð Iacob: Gif gē nīede swā dōn sculon, dōð swā gē willað; nimað of ēowrum bętstum wæstmum on fatum, and bringað ðām męn lāc, hunig and æcern.'
],45:[
'Nimað ēowerne brōðor and gāð tō ðām męn.',
'And mīn Drihten gedō hine glædne wið ēow, ðæt hē ēow ēowerne brōðor āgiefe, ðe hē mid him hæfð; ic eom nū mīnra bearna berēafod.',
'Ðā nāmon hīe ðā lāc and twīfeald feoh, and fērdon tō Egypta lande tō Iosepe.',
'Ðā hē hīe geseah, ðā cwæð hē tō his gerēfan: Lǣd ðās męnn in, and gearca ūrne gebeorscipe, ðæt hīe mægen mid mē etan tō middes dæges.',
'And hē dyde swā him boden wæs.',
'Ðā hīe ðǣr wǣron, ðā wurdon hīe swīðe āfyrhte, and sægdon betweonan him: For ðām fēo ðe wē on ūrum saccum fundon, wē sind hider in gelǣdde, ðæt hē ūs ūrra assa and ūrra ðinga berēafie, and ūs selfe geðēowie.',
'Ðā cwǣdon hīe tō ðām gerēfan: Ēalā hlāford, wē biddað ðæt ðū ūre sprǣce hlyste; wē wǣron hēr hwīlum ǣr and bohton ūs hwǣte.',
'Ðā wē cēapodon and hāmweard wǣron, ðā undydon wē ūre saccas; ðā fundon wē ðæt feoh ðǣron ðe wē ǣr sealdon.',
'Nū wē hit ęft brōhton, and ēac ōðer siolfor mid tō cēapianne; and wē ne witon hwā hit on ūre saccas dyde.'
],46:[
'Ðā cwæð se gerēfa: Sibb sīe mid ēow; ne ondrǣdað ēow; ēower God and ēower fæder God sealde ēow goldhord on ēowrum saccum.',
'And hīe ðwōgon hiera fēt, and hē sealde hiera assum fodor.',
'Hīe lęgdon hiera lāc forð, ongēan ðætte Iosep incōme.',
'Ðā oncnēow Iosep hīe, and āscode hwæðer hiera fæder hāl wǣre, oððe hwæðer hē leofode.',
'Ðā cwǣdon hīe: Ðīn ðēow, ūre fæder, is gesund; hē leofað gīet.',
'Ðā Iosep geseah his brōðor Beniamin, ðā cwæð hē: Is ðis se cnapa ðe gē foresægdon? And hē cwæð: God gemiltsie ðē, mīn sunu.',
'Ðā bēad Iosep his gerēfan, and cwæð: Gefyll hiera saccas mid hwǣte, and sęte ǣlces hiera feoh on his āgenne sacc.',
'And nim mīnne siolforlæfel, and ðæs hwǣtes weorð ðe hē him sealde, and dō hit on ðæs gingstan sacc; and hē dyde swā.',
'On morgen, ðā hīe fērdon, and hīe būton wǣron, and hæfdon sumne dǣl ðæs weges gefaren, ðā cwæð Iosep tō his gerēfan: Ārīs, and gā æfter ðām mannum; and ðonne gē hīe gelǣccen, ðonne āsciað hīe hwȳ hīe wolden gōd mid yfele forgieldan.'
],47:[
'Se læfel ðe gē forstǣlon wæs mīnum hlāforde swīðe dēorwierðe.',
'Hē dyde swā him boden wæs, and ðā hīe gelǣhte wǣron, ðā cwǣdon hīe: Ðæt feoh ðe wē on ūrum saccum fundon, wē brōhton ðē of ūrum lande; wēnst ðū ðæt wē ðæs hlāfordes gold oððe his siolfor stǣlen?',
'Sēc hit; and sīe hē ofslægen mid ðǣm ðū hit finde.',
'Ðā cwæð hē: Mid swā hwām swā ic hit finde, sīe hē mīn ðēow, and sīen ðā ōðre clǣne.',
'And hē sōhte fram ðām ieldestan oð ðone gingstan; and hē fand ðone læfel on Beniamines sacce; and hīe ęft gewęndon tō ðǣre byrig.',
'And Iudas ēode in fyrmest mid his brōðrum tō Iosepe, and hīe ealle ætgædere beforan Iosepe fēollon.',
'And hē cwæð tō him: Hwȳ gē swā dōn woldon?',
'Sīe hē mīn ðēow ðe ðone læfel forstæl, and gāð gē frige tō ēowrum fæder.',
'Ðā cwæð Iudas: Ðū āscodest ūs hwæðer wē fæder oððe brōðor hæfden.',
'And wē cwǣdon: Wē habbað ealdne fæder, and hē hæfð mid him ūrne gingstan brōðor; and hē lufað hine ænne ofer ūs ealle.',
'And ðū bīetst ūs ðæt wē hine ðē bringen, ðæt ðū hine gesēo, and wite be ðām ðæt wē ne scēaweras sindon.'
],48:[
'And ic swōr āðas mīnum fæder ðæt ic hine ęft hām tō him brōhte, and cwæð: Būton ic hine ęft tō ðē bringe, sīe ic ā scyldig wið ðē.',
'Mīn hlāford, lǣt ðone cnapan mid his brōðrum gān, and sīe ic ðīn ðēow for hine.',
'Ic ne dearr hām gān būton ðām cnapan, ðȳlǣs ic mīnes fæder sārnesse gesēo.',
'Ðā ne meahte Iosep hine lęng diernan, ac hē ādrāf ealle ðā ōðre ūt, ðæt nān ęlðēodig mann betweox him nǣre.',
'And hē wēop and cleopode hlūdre stefne; and hē cwæð tō his brōðrum: Ic eom Iosep; leofað ūre fæder nū gīet?',
'Ne ondrǣdað ēow nānes ðinges, ne ofðynce ēow ðæt gē mē on ðis rīce sealdon; sōðlice God sęnde mē for ēowre ðearfe tō Egypta lande.',
'Nū twā gēar hungor wæs ofer eorðan, and gīet sculon fīf, on ðǣm mann nāðor ne erian ne rīpan mæg.',
'Gāð hrædlīce tō mīnum fæder and sęcgað him ðæt God mē tō hlāforde ofer Egyptum gesętte; bēodað him ðæt hē tō mē cume and on ðissum lande wun ie.',
'Dōð ðis, ðæt wē ne forweorðen.',
'Nū gē gesēoð hū hit mid mē is, and gē hīerað hwæt ic tō ēow sprece.'
]}
rows=[]
for ex,models in M.items():
 for n,model in enumerate(models,1):
  model=model.replace('wun ie','wunie')
  rows.append({'item_id':f'EX-XII-XIII-{ex:02}-{n:02}','exercise':ex,'item':n,'model':model,'origin_category':'new teaching material; independent proposed composition for exact Cook prompt','status':'provisional linguistic hypothesis; lexical evidence and controls not yet sealed','pending':'Exact source hints, lexical stems/senses and constructions must be reconciled before contract.'})
assert len(rows)==47
(O/'candidate-models.json').write_text(json.dumps({'schema_version':1,'status':'precontract hypotheses, not learner/key prose','author':'unit18_grammar','baseline':'0eda277','items':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('47 hypotheses saved; do not assign until evidence reconciled.')
