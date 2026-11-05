from pathlib import Path
import json,csv,re,difflib
OUT=Path(r'C:\YOUTUBE\Youtube 2\Glomar Explorer\AUDIO\R1_2_MASTER_ASR')
small='zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen'.split();tens='zero ten twenty thirty forty fifty sixty seventy eighty ninety'.split()
def number(n):
 if n<20:return small[n]
 if n<100:return tens[n//10]+(' '+small[n%10] if n%10 else '')
 if n<1000:return small[n//100]+' hundred'+(' '+number(n%100) if n%100 else '')
 if 1900<=n<2000:return 'nineteen '+('oh '+number(n%100) if n%100<10 else number(n%100))
 if 2000<=n<2100:return 'two thousand'+(' '+number(n%100) if n%100 else '')
 return number(n//1000)+' thousand'+(' '+number(n%1000) if n%1000 else '')
def norm(text):
 text=text.lower().replace('’',"'")
 text=re.sub(r'(?<=\d),(?=\d)','',text)
 text=re.sub(r'(?<=[a-z])(?=\d)|(?<=\d)(?=[a-z])',' ',text)
 text=re.sub(r'\b(\d+) ?(st|nd|rd|th)\b',r'\1',text)
 text=re.sub(r'\b\d{1,6}\b',lambda m:number(int(m.group())),text)
 text=re.sub(r'\bhundred and\b','hundred',text);text=re.sub(r'\btwenty (fifteen|sixteen)\b',lambda m:'two thousand '+m.group(1),text)
 text=text.replace("can't",'cannot').replace("couldn't",'could not').replace("wouldn't",'would not').replace("didn't",'did not').replace("it's",'it is')
 text=text.replace('centre','center').replace('undercover','under cover').replace('trans ocean','transocean').replace('gimballed','gimbaled').replace('gimbaled','gimballed')
 return re.findall(r"[a-z]+(?:'[a-z]+)?",text)
def ops(a,b):return [{'type':t,'expected':' '.join(a[i:j]),'recognized':' '.join(b[k:l]),'expected_index':i,'recognized_index':k} for t,i,j,k,l in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes() if t!='equal']
