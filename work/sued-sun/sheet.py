from PIL import Image
import glob,sys
fs=sorted(glob.glob('test/t*.jpg'));W,H=270,480;cols=7;rows=(len(fs)+cols-1)//cols
sh=Image.new('RGB',(W*cols,H*rows),'black')
for i,f in enumerate(fs):sh.paste(Image.open(f).resize((W,H)),((i%cols)*W,(i//cols)*H))
sh.save('test/sheet.jpg',quality=85)
