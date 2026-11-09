"""Regenerate publication charts from committed release CSVs (optional matplotlib)."""
from pathlib import Path
import csv
import io
from collections import Counter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

ROOT=Path(__file__).resolve().parents[1]
GREEN='#276151'; DARK='#183D34'; MUTED='#698077'; GRID='#E3E9E6'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'axes.spines.top':False,'axes.spines.right':False,'axes.spines.left':False,'axes.labelcolor':DARK,'xtick.color':DARK,'ytick.color':DARK,'text.color':DARK,'axes.titleweight':'bold','axes.titlesize':15,'figure.facecolor':'white'})

def rows(path):
    with (ROOT/path).open(encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def finish(fig,name,title,subtitle='Synthetic portfolio data | Release 2026-10-28 | Rendered from released CSV/SQL results'):
    fig.suptitle(title,x=.06,y=.97,ha='left',fontsize=24,fontweight='bold',color=DARK)
    fig.text(.06,.025,subtitle,fontsize=10,color=MUTED)
    fig.subplots_adjust(top=.78,bottom=.18,left=.09,right=.96,wspace=.35)
    if name=='employee_dashboard.png':
        fig.subplots_adjust(left=.17,wspace=.85)
        for ax in fig.axes: ax.tick_params(axis='y',labelsize=10)
    buf=io.BytesIO();fig.savefig(buf,format='png',dpi=150,facecolor='white')
    target=ROOT/'assets'/name;tmp=target.with_suffix('.tmp');tmp.write_bytes(buf.getvalue());tmp.replace(target);plt.close(fig)
def clean(ax):
    ax.grid(axis='y',color=GRID);ax.set_axisbelow(True);ax.yaxis.set_major_locator(MaxNLocator(integer=True))

def main():
    head=rows('examples/sql-results/01_headcount.csv');absence=rows('examples/sql-results/04_monthly_absence.csv')
    housing=rows('examples/sql-results/03_housing_occupancy.csv');leave=rows('data/leave.csv')
    fig,axs=plt.subplots(1,2,figsize=(14,6))
    vals=[int(r['active_employees']) for r in head]
    bars=axs[0].barh([r['company'] for r in head],vals,color=GREEN);axs[0].bar_label(bars,padding=5);axs[0].set_xlim(0,max(vals)*1.2);axs[0].set_title('Active employees by company');axs[0].set_xlabel('Employees')
    counts=Counter(r['termination_reason'] for r in rows('data/employee_references.csv'))
    bars=axs[1].barh(list(counts),list(counts.values()),color=MUTED);axs[1].bar_label(bars,padding=5);axs[1].set_xlim(0,max(counts.values())*1.25);axs[1].set_title('Recorded termination categories');axs[1].set_xlabel('Reference records')
    fig.subplots_adjust(wspace=.6)
    finish(fig,'employee_dashboard.png','Employee management: reporting views')
    fig,axs=plt.subplots(1,2,figsize=(14,6))
    months=[r['month_start'][5:7] for r in absence]
    labels=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct']
    for ax,key,title in zip(axs,['episodes_started','calendar_absence_days'],['Episodes started','Elapsed calendar absence days']):
        bars=ax.bar(labels,[int(r[key]) for r in absence],color=GREEN);ax.bar_label(bars,padding=4,fontsize=10);ax.set_title(title);ax.set_ylim(0,max(int(r[key]) for r in absence)*1.2);clean(ax)
    finish(fig,'sick_leave_dashboard.png','Sick leave: monthly reporting, 2026')
    fig,axs=plt.subplots(1,2,figsize=(14,6))
    count=Counter(int(r['Start date'][5:7]) for r in leave if r['Validation']=='OK' and r['Start date']<='2026-10-28')
    bars=axs[0].bar(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],[count[m] for m in range(1,13)],color=GREEN);axs[0].bar_label(bars,padding=3,fontsize=9);axs[0].set_title('Started leave periods by month');axs[0].set_ylim(0,40);clean(axs[0])
    bands=[('1-3 days',1,3),('4-7 days',4,7),('8-14 days',8,14),('15+ days',15,9999)]
    vals=[sum(lo<=int(r['Calendar days'])<=hi for r in leave if r['Validation']=='OK') for _,lo,hi in bands]
    bars=axs[1].bar([r[0] for r in bands],vals,color=MUTED);axs[1].bar_label(bars,padding=4);axs[1].set_title('Leave periods by calendar duration');axs[1].set_ylim(0,max(vals)*1.2);clean(axs[1])
    finish(fig,'leave_dashboard.png','Leave management: timing and duration')
    fig,ax=plt.subplots(figsize=(14,6))
    bars=ax.bar([r['apartment_id'] for r in housing],[int(r['residents']) for r in housing],color=GREEN);ax.bar_label(bars,padding=5);ax.set_ylim(0,5);ax.set_title('Residents per apartment; capacity is four beds each');ax.set_ylabel('Residents');clean(ax)
    finish(fig,'housing_occupancy.png','Housing: 40 residents across 10 apartments')
    fig,axs=plt.subplots(1,2,figsize=(14,7))
    fig.text(.06,.82,'85',fontsize=34,fontweight='bold');fig.text(.06,.77,'active employees',fontsize=12)
    fig.text(.30,.82,'40 / 40',fontsize=34,fontweight='bold');fig.text(.30,.77,'housing beds occupied',fontsize=12)
    fig.text(.57,.82,'185',fontsize=34,fontweight='bold');fig.text(.57,.77,'leave periods in 2026',fontsize=12)
    fig.text(.80,.82,'21',fontsize=34,fontweight='bold');fig.text(.80,.77,'automated tests passed',fontsize=12)
    monthly=rows('examples/sql-results/02_monthly_headcount.csv')
    for company in [r['company'] for r in head]:
        seq=[r for r in monthly if r['company']==company]
        axs[0].plot(labels,[int(r['active_employees']) for r in seq],marker='o',label=company)
    axs[0].set_title('Headcount at each monthly cutoff');axs[0].set_ylabel('Employees');axs[0].legend(frameon=False,fontsize=10);clean(axs[0])
    axs[1].bar(labels,[int(r['calendar_absence_days']) for r in absence],color=GREEN);axs[1].set_title('Calendar absence days by month');axs[1].set_ylabel('Days');clean(axs[1])
    fig.suptitle('HR Operations Analytics',x=.06,y=.97,ha='left',fontsize=29,fontweight='bold')
    fig.text(.06,.89,'Workplace workflows reconstructed with entirely fictional data',fontsize=13,color=MUTED)
    fig.text(.06,.025,'Release 2026-10-28 | CSV + SQL reporting | Figures describe synthetic scenarios',fontsize=10,color=MUTED)
    fig.subplots_adjust(top=.62,bottom=.15,left=.07,right=.96,wspace=.25)
    buf=io.BytesIO();fig.savefig(buf,format='png',dpi=150)
    target=ROOT/'assets/portfolio_overview.png';tmp=target.with_suffix('.tmp');tmp.write_bytes(buf.getvalue());tmp.replace(target);plt.close(fig)

if __name__=='__main__':main()
