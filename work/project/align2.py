import subprocess,re,json
def segs_of(vo,noise='-38dB',min_sil=0.22):
    r=subprocess.run(['ffmpeg','-i',vo,'-af',f'silencedetect=noise={noise}:d={min_sil}','-f','null','-'],capture_output=True,text=True).stderr
    ev=re.findall(r'silence_(start|end): ([0-9.]+)',r); sil=[];cur=None
    for k,v in ev:
        v=float(v)
        if k=='start':cur=v
        else: sil.append((cur or 0,v));cur=None
    total=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',vo],capture_output=True,text=True).stdout)
    if cur is not None: sil.append((cur,total))
    segs=[];t=0
    for a,b in sil:
        if a>t+0.05: segs.append((t,a))
        t=b
    if t<total-0.05: segs.append((t,total))
    return segs,total
def ch(l): return len(re.sub(r'\[.*?\]','',l))
def dp_align(segs,lines,rate,maxk=8,forced=set()):
    n,m=len(lines),len(segs);INF=1e18
    dp=[[INF]*(m+1) for _ in range(n+1)];bk=[[0]*(m+1) for _ in range(n+1)];dp[0][0]=0
    for i in range(1,n+1):
        for j in range(i,m+1):
            for k in range(max(i-1,j-maxk),j):
                if dp[i-1][k]>=INF: continue
                if any(k<f<j for f in forced): continue   # a line can't span a part join
                dur=segs[j-1][1]-segs[k][0];exp=ch(lines[i-1])*rate
                gap=segs[k][0]-(segs[k-1][1] if k>0 else 0)
                c=dp[i-1][k]+((dur-exp)/(exp+0.5))**2-0.15*min(gap,1.5)
                if c<dp[i][j]:dp[i][j]=c;bk[i][j]=k
    j=m;out=[]
    for i in range(n,0,-1):
        k=bk[i][j];out.append((segs[k][0],segs[j-1][1]));j=k
    return out[::-1],dp[n][m]
