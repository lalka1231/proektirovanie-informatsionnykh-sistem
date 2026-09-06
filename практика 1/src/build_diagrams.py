from pathlib import Path
import subprocess
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
P=Path(__file__).resolve().parents[1]
D=P/'diagrams'; R=D/'rendered'
style='''!pragma layout smetana
skinparam backgroundColor #FFFFFF
skinparam defaultFontName Arial
skinparam defaultFontSize 21
skinparam shadowing false
skinparam ArrowColor #324A60
skinparam roundcorner 14
skinparam activityBackgroundColor #E8F3F4
skinparam activityBorderColor #247E83
skinparam usecaseBackgroundColor #E8F3F4
skinparam usecaseBorderColor #247E83
skinparam rectangleBorderColor #324A60
skinparam componentBackgroundColor #E8F3F4
skinparam componentBorderColor #247E83
skinparam noteBackgroundColor #FFF2D7
skinparam noteBorderColor #C88C30
'''
items={
'as_is':r'''title AS-IS: подготовка и выполнение дневного маршрута
|PFT — существующая ИС|
start
:Задания, адреса,\nограничения обслуживания;
|Планировщик|
:Проверить задания\nи условия доставки;
|Водитель|
:Уточнить порядок остановок\nна основе опыта;
note right
Ручной выбор последовательности:
не все варианты сопоставлены
end note
:Выполнить доставки\nи заборы отправлений;
if (Возникло отклонение?) then (да)
:Повторно оценить порядок\nи согласовать действия;
note right
Возврат к ручному решению;
риск лишнего пробега и задержки
end note
else (нет)
endif
:Передать сведения\nо выполнении;
stop
legend bottom
Учебная реконструкция процесса на основании [1].
До ORION уже применялась PFT; бумажный документооборот не предполагается.
endlegend
''',
 'to_be':r'''title TO-BE: те же задания — оптимизированный порядок
|PFT — существующая ИС|
start
:Задания, адреса,\nограничения обслуживания;
|ORION — автоматически|
:Проверить входные данные\nи картографическую основу;
if (Данные пригодны?) then (да)
:Рассчитать порядок остановок\nс учетом ограничений;
:Передать маршрут водителю;
else (нет)
|Планировщик|
:Приостановить расчет\nи разобрать ошибки данных;
note right
После исправления — новый расчет.
При невозможности — резервный план.
end note
stop
endif
|Водитель|
:Выполнить доставки\nи заборы отправлений;
if (Возникло отклонение?) then (да)
:Разобрать исключение\nс планировщиком;
else (нет)
endif
:Передать сведения\nо выполнении;
stop
legend bottom
Учебная реконструкция на основании [1].
Контур 2016 года: постоянный пересчет в пути не приписывается этой версии.
endlegend
''',
'use_case':r'''left to right direction
actor "Планировщик" as planner
actor "Водитель" as driver
actor "Руководитель\nдоставки" as manager
rectangle "ORION — учебная граница системы" {
usecase "Сформировать\nмаршрут" as route
usecase "Проверить\nисходные данные" as validate
usecase "Получить\nмаршрут" as receive
usecase "Оценить\nвыполнение" as assess
route .> validate : <<include>>
}
actor "PFT\n(внешняя ИС)" as pft
actor "Сервис карт\n(внешняя роль)" as maps
planner -- route
driver -- receive
manager -- assess
pft -- route
maps -- validate
legend bottom
UML Use Case. Реконструкция требований, не официальная диаграмма UPS [1].
Сервис карт — роль картографического контура, не утверждение об отдельном поставщике.
endlegend
''',
'architecture':r'''top to bottom direction
rectangle "Пользовательские каналы — реконструкция" {
[Рабочее место\nпланировщика] as desktop
[Клиент\nводителя] as mobile
[Просмотр\nрезультатов] as report
}
rectangle "Прикладной слой ORION" {
[Прием данных и\nконтроль качества «Р»] as input
[Ядро оптимизации UPS «Ф»\nПорядок остановок с ограничениями] as engine
[Выдача маршрута\nи анализ выполнения «Р»] as output
input -right-> engine
engine -right-> output
}
rectangle "Логический слой данных — реконструкция" {
database "Задания и ограничения\nВерсии маршрутов и результаты\nФизическая СУБД не установлена" as db
}
cloud "PFT «Ф»\nСуществующая платформа UPS" as pft
cloud "Картографические данные «Ф»\nСпособ интеграции — «Р»" as maps
desktop --> input : запрос
output --> mobile : маршрут
output --> report : показатели
pft --> input : задания
maps --> input : дорожная сеть
input --> db
engine --> db
output --> db
legend bottom
Реконструированная архитектура на основании доступного описания решения [1].
«Ф» — подтверждено; «Р» — реконструкция. Развертывание, протоколы и СУБД не опубликованы.
endlegend
''',
'lifecycle':r'''left to right direction
rectangle "1. Планирование\nи требования" as a
rectangle "2. Проектирование\nданных и ограничений" as b
rectangle "3. Реализация\nи полевые проверки" as c
rectangle "4. Внедрение\nпо площадкам" as d
rectangle "5. Эксплуатация\nи контроль эффекта" as e
a --> b
b --> c
c --> b : обратная связь
c --> d : входные критерии
d --> e : выходные критерии
e --> b : новые требования
legend bottom
Наиболее подходящая модель ЖЦ: итерационная разработка + инкрементальное внедрение.
Реконструкция. Полевые тесты, критерии готовности и контроль метрик подтверждены [1].
endlegend
''',
'future_technology':r'''left to right direction
rectangle "История остановок\nКонтекст маршрута\nБез лишних персональных данных" as a
rectangle "Машинное обучение\nПрогноз длительности\n+ неопределенность" as b
rectangle "Оптимизатор\nРезерв времени\nпри высоком риске" as c
rectangle "Человек\nКонтроль исключений\nи качества сервиса" as d
a --> b
b --> c
c --> d
d --> a : фактическое время
legend bottom
Авторское предложение: не утверждение о текущих возможностях UPS.
Эффект проверяется в пилоте; при недоверии к модели — базовый расчет.
endlegend
'''}
for name,body in items.items():
    (D/f'{name}.puml').write_text('@startuml\n'+style+body+'@enduml\n',encoding='utf-8')
cmd=['java','-Djava.awt.headless=true','-jar',str(P/'src/plantuml.jar'),'-charset','UTF-8','-tpng','-o','rendered']+[str(D/f'{n}.puml') for n in items]
subprocess.run(cmd,check=True)
subprocess.run([*cmd[:],],check=True) if False else None
# Оценочный график одной площадки, относительные недели, без ложных календарных дат.
rows=[('Анализ требований',0,3),('Проектирование и качество данных',2,4),('Настройка и интеграция',5,5),('Пилот и корректировки',9,4),('Обучение и ввод',12,3),('Стабилизация и приемка',14,3)]
import csv
with (D/'gantt.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.writer(f);w.writerow(['этап','начало_неделя_с_нуля','длительность_недели']);w.writerows(rows)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':16})
fig,ax=plt.subplots(figsize=(14,5.5),layout='constrained')
for i,(name,start,duration) in enumerate(rows):
    ax.barh(i,duration,left=start,color='#247E83' if i%2==0 else '#324A60',height=.58)
    ax.text(start+duration/2,i,f'{duration} нед.',ha='center',va='center',color='white',fontsize=14)
ax.set_yticks(range(len(rows)),[r[0] for r in rows]);ax.invert_yaxis();ax.set_xlim(0,17);ax.set_xticks(range(0,18),[str(x+1) for x in range(18)]);ax.set_xlabel('Относительная неделя проекта одной площадки');ax.grid(axis='x',alpha=.14);ax.set_axisbelow(True)
for sp in ax.spines.values():sp.set_visible(False)
fig.suptitle('Учебная реконструкция графика проекта',fontsize=21,fontweight='bold')
fig.text(.5,.005,'Точные сроки в открытых источниках не опубликованы. Длительности — авторская оценка, не график UPS.',ha='center',fontsize=11,color='#596B7C')
fig.savefig(R/'gantt_estimate.png',dpi=180,bbox_inches='tight');plt.close(fig)
(D/'gantt_estimate.csv').write_text((D/'gantt.csv').read_text(encoding='utf-8'),encoding='utf-8')
# Исторический график с годовой точностью: полоса — названные годы, маркер — событие.
fig,ax=plt.subplots(figsize=(14,5),layout='constrained')
ax.barh(1,4,left=2008,height=.52,color='#247E83')
ax.text(2010,1,'2008–2011: прототипирование [5]',ha='center',va='center',color='white',fontsize=15)
for year,row,label in [(2003,0,'Начало исследований [1]'),(2008,2,'Первый полевой тест [1]'),(2013,3,'Официальный запуск [5]'),(2016,4,'Завершение внедрения [1]')]:
    ax.scatter(year+.5,row,s=135,marker='D',color='#C88C30',zorder=4)
    ax.text(year+.72 if year<2013 else year+.25,row-.25,label,ha='left' if year<2013 else 'right',va='center',fontsize=15,color='#20364D')
ax.set_xlim(2002.8,2017.2);ax.set_ylim(4.65,-.75);ax.set_yticks([])
ax.set_xticks([x+.5 for x in range(2003,2017)],list(range(2003,2017)),rotation=0,fontsize=12)
ax.grid(axis='x',alpha=.15);ax.set_axisbelow(True)
ax.set_xlabel('Годы. Положение маркера внутри года условно; месяцы не установлены.',fontsize=13)
for sp in ax.spines.values():sp.set_visible(False)
fig.suptitle('Гант и вехи по фактическим сведениям: точность до года',fontsize=20,fontweight='bold')
fig.savefig(R/'gantt.png',dpi=180,bbox_inches='tight');plt.close(fig)
with (D/'gantt.csv').open('w',encoding='utf-8',newline='') as f:
    writer=csv.writer(f);writer.writerow(['событие_или_этап','тип','начальный_год','конечный_год','источник']);writer.writerows([['Начало исследований','веха',2003,2003,'[1]'],['Прототипирование','период',2008,2011,'[5]'],['Первый полевой тест','веха',2008,2008,'[1]'],['Официальный запуск','веха',2013,2013,'[5]'],['Завершение внедрения','веха',2016,2016,'[1]']])
# Было/стало: абсолютные базовые значения неизвестны, показываем дельты, не фиктивные столбцы.
fig,ax=plt.subplots(figsize=(14,4.8));ax.axis('off')
for x,title,txt,c in [(0.02,'БЫЛО','PFT + опыт водителя\n\nОбщий пробег и затраты\nв источнике не раскрыты','#EEF1F4'),(.53,'СТАЛО','PFT + ORION\n\n−100 млн миль / год\n$300–400 млн / год экономии','#E5F3F1')]:
    ax.add_patch(FancyBboxPatch((x,.12),.44,.76,boxstyle='round,pad=0.02',facecolor=c,edgecolor='none'))
    ax.text(x+.025,.77,title,fontsize=22,fontweight='bold',color='#20364D')
    ax.text(x+.025,.61,txt,fontsize=21,va='top',color='#20364D',linespacing=1.5)
ax.text(.495,.5,'→',fontsize=28,ha='center',color='#247E83')
ax.text(.02,.02,'Оценки UPS в интервью 2017 года [1]. Эффект ORION отдельно от PFT. Процент снижения не вычисляется.',fontsize=12,color='#596B7C')
fig.savefig(R/'results.png',dpi=180,bbox_inches='tight');plt.close(fig)
print('Rendered:',[(x.name,x.stat().st_size) for x in R.glob('*.png')])
