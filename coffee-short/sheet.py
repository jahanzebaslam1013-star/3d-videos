from PIL import Image,ImageDraw
import glob,sys
fs=sorted(glob.glob('test/t*.jpg'));W=270;H=480;cols=8;rows=(len(fs)+cols-1)//cols
sheet=Image.new('RGB',(cols*W,rows*H),'black')
for i,f in enumerate(fs):
    im=Image.open(f).resize((W,H));d=ImageDraw.Draw(im);d.line([(0,H*.71),(W,H*.71)],fill=(255,0,0));d.text((5,5),str(i),fill=(255,255,0));sheet.paste(im,((i%cols)*W,(i//cols)*H))
sheet.save(sys.argv[1] if len(sys.argv)>1 else 'contact.jpg');print(sheet.size)
