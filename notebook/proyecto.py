import os,sys;from collections import Counter;import pandas as pd
if "google.colab" not in sys.modules:import matplotlib;matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":120,"axes.spines.top":False,"axes.spines.right":False,"axes.titlesize":11,"axes.labelsize":9})
RESULTADOS=os.path.join(os.getcwd(),"resultados");os.makedirs(RESULTADOS,exist_ok=True);INF=float("inf")
POOL=[dict(zip("id programa semestre ciudad jornada".split(),r))for r in[
(1,"Computacion",1,"Manizales","Diurna"),(2,"Matematicas",1,"Pereira","Diurna"),(3,"Estadistica",2,"Armenia","Nocturna"),(4,"Computacion",2,"Manizales","Diurna"),(5,"Matematicas",3,"Pereira","Nocturna"),
(6,"Estadistica",1,"Armenia","Diurna"),(7,"Fisica",3,"Manizales","Diurna"),(8,"Computacion",1,"Pereira","Nocturna"),(9,"Matematicas",4,"Manizales","Diurna"),(10,"Estadistica",2,"Pereira","Diurna"),
(11,"Computacion",3,"Armenia","Nocturna"),(12,"Fisica",1,"Manizales","Diurna"),(13,"Matematicas",2,"Armenia","Nocturna"),(14,"Computacion",4,"Pereira","Diurna"),(15,"Estadistica",3,"Manizales","Nocturna"),
(16,"Fisica",2,"Armenia","Diurna"),(17,"Computacion",1,"Armenia","Diurna"),(18,"Matematicas",5,"Pereira","Nocturna"),(19,"Estadistica",4,"Manizales","Diurna"),(20,"Fisica",5,"Armenia","Nocturna")]]
C1={"nombre":"Conjunto 1 — Base","tamano":6,"min_programa":{"Computacion":2,"Matematicas":1},"max_por_ciudad":3,"min_semestre_1":2,"min_nocturna":0}
C2={"nombre":"Conjunto 2 — Alta diversidad","tamano":6,"min_programa":{"Computacion":2,"Matematicas":1,"Estadistica":1},"max_por_ciudad":3,"min_semestre_1":1,"min_nocturna":2}
C3={"nombre":"Conjunto 3 — Sin solución","tamano":7,"min_programa":{"Computacion":2,"Matematicas":1},"max_por_ciudad":2,"min_semestre_1":2,"min_nocturna":0}
def _cnt(m):
    return Counter(e["programa"]for e in m),Counter(e["ciudad"]for e in m),Counter(e["jornada"]for e in m),sum(1 for e in m if e["semestre"]==1)
def _podar(m,r,q):
    f=q["tamano"]-len(m);p,c,j,s=_cnt(m);mc=q.get("max_por_ciudad",INF)
    if mc<INF and sum(max(0,mc-c.get(x,0))for x in set(e["ciudad"]for e in r)|set(c))<f:return True
    ef=[e for e in r if c.get(e["ciudad"],0)<mc]if mc<INF else r
    return len(ef)<f or any(p.get(k,0)+sum(1 for e in ef if e["programa"]==k)<v for k,v in q["min_programa"].items())or s+sum(1 for e in ef if e["semestre"]==1)<q["min_semestre_1"]or j.get("Nocturna",0)+sum(1 for e in ef if e["jornada"]=="Nocturna")<q["min_nocturna"]
def backtracking(pool,m,q,sols,cnt,i0=0,lim=1):
    cnt["llamadas_recursivas"]+=1
    if len(m)==q["tamano"]:
        p,_,j,s=_cnt(m);(sols.append(list(m))if all(p.get(k,0)>=v for k,v in q["min_programa"].items())and s>=q["min_semestre_1"]and j.get("Nocturna",0)>=q["min_nocturna"]else None);return
    if lim and len(sols)>=lim:return
    r=pool[i0:]
    if _podar(m,r,q):cnt["ramas_descartadas"]+=1;return
    mc=q.get("max_por_ciudad",INF);ciu=Counter(e["ciudad"]for e in m)
    for i,e in enumerate(r):
        if lim and len(sols)>=lim:return
        if ciu.get(e["ciudad"],0)<mc:m.append(e);backtracking(pool,m,q,sols,cnt,i0+i+1,lim);cnt["retrocesos"]+=1;m.pop()
        else:cnt["ramas_descartadas"]+=1
def buscar(q,pool=None,lim=1,v=True):
    pool=pool or POOL;s,c=[],{"llamadas_recursivas":0,"ramas_descartadas":0,"retrocesos":0};backtracking(pool,[],q,s,c,lim=lim)
    if not v:return s,c
    print(f"\n{'='*55}\n  {q['nombre']}\n  Tam:{q['tamano']} Llamadas:{c['llamadas_recursivas']} Descartadas:{c['ramas_descartadas']} Retrocesos:{c['retrocesos']} Sol:{len(s)}")
    if s:print(pd.DataFrame(s[0]).to_string(index=False));p,_,j,z=_cnt(s[0]);print(f"  prog={dict(p)} sem1={z}>={q['min_semestre_1']} noct={j.get('Nocturna',0)}>={q['min_nocturna']}")
    else:print(f"  *** SIN SOLUCION *** {q['max_por_ciudad']}x3={3*q['max_por_ciudad']}<{q['tamano']}")
    return s,c
s1,c1=buscar(C1);s2,c2=buscar(C2);s3,c3=buscar(C3)
fig,axes=plt.subplots(2,3,figsize=(14,8));fig.suptitle("Pool original vs. Muestras seleccionadas",fontsize=13,fontweight="bold")
for row,(m,q,col) in enumerate([(s1[0],C1,"#4472C4"),(s2[0],C2,"#ED7D31")]):
    for ax,f in zip(axes[row],["programa","ciudad","jornada"]):
        cp,cm,w=Counter(e[f]for e in POOL),Counter(e[f]for e in m),0.35;cats=sorted(cp);x=range(len(cats))
        [ax.bar([i-w/2 for i in x],[cp[c]for c in cats],w,color="#4472C4",alpha=.85,label=f"Pool({len(POOL)})"),ax.bar([i+w/2 for i in x],[cm.get(c,0)for c in cats],w,color="#ED7D31",alpha=.85,label=f"Muestra({len(m)})")]
        ax.set_xticks(list(x));ax.set_xticklabels(cats,rotation=25,ha="right",fontsize=8);ax.set_title(f"Por {f}",fontsize=9);ax.set_ylabel("N",fontsize=8);ax.legend(fontsize=7)
    axes[row][0].annotate(q["nombre"],xy=(.5,1.12),xycoords="axes fraction",ha="center",fontsize=9,fontweight="bold",color=col)
plt.tight_layout();plt.savefig(f"{RESULTADOS}/comparacion_distribuciones.png",dpi=150,bbox_inches="tight");plt.show()
fig,(ax1,ax2)=plt.subplots(1,2,figsize=(11,4));fig.suptitle("Eficiencia del backtracking",fontsize=12,fontweight="bold")
for ax,vals,t in[(ax1,[c1["llamadas_recursivas"],c2["llamadas_recursivas"],c3["llamadas_recursivas"]],"Llamadas recursivas"),(ax2,[c1["ramas_descartadas"],c2["ramas_descartadas"],c3["ramas_descartadas"]],"Ramas descartadas")]:
    ax.bar(["C1","C2","C3"],vals,color=["#4472C4","#ED7D31","#A9D18E"],alpha=.87,edgecolor="white");ax.set(title=t,ylabel="Cantidad");[ax.text(i,v+max(vals)*.01,str(v),ha="center",fontsize=9,fontweight="bold")for i,v in enumerate(vals)]
plt.tight_layout();plt.savefig(f"{RESULTADOS}/eficiencia_backtracking.png",dpi=150,bbox_inches="tight");plt.show()
def balance(m,pool=POOL):
    n,k,cp,cm=len(pool),len(m),Counter(e["programa"]for e in pool),Counter(e["programa"]for e in m);return round(1-sum(abs(cp[p]/n-cm.get(p,0)/k)for p in cp),4)
st,_=buscar(C1,lim=None,v=False);sc=[balance(m)for m in st];best=st[sc.index(max(sc))]
print(f"Muestras validas:{len(st)} | score max:{max(sc)} | prom:{round(sum(sc)/len(sc),4)} | min:{min(sc)}\n{pd.DataFrame(best).to_string(index=False)}")
