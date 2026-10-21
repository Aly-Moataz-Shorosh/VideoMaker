"""<video>.txt beside every short in output/shorts: 3 titles, description (+ link to the full episode), hashtags, pinned comment.
python make_txt.py  (all shorts that have a video)"""
import sys
from pathlib import Path
from shorts_data import SHORTS
sys.stdout.reconfigure(encoding='utf-8')
P = Path(__file__).resolve().parents[2]
OUT = P / 'output' / 'shorts'
LINK = 'https://youtu.be/5xqomlWcKzE'

# n: (3 titles, one-line summary, hashtags, pinned-comment question)
META = {
    1: (['الـDeveloper بيفكر إزاي تشتغل.. والـTester إزاي متشتغلش', 'ليه الشركة محتاجة Tester لو الـDeveloper شاطر؟', 'عين الـDeveloper وعين الـTester'],
        'المشكلة مش إن الـDeveloper شاطر ولا لأ: كل واحد عنده Mindset مختلف، والـTester بيشوف من أكتر من زاوية.',
        '#SoftwareTesting #QA #Developer', 'إنت Developer ولا Tester؟'),
    2: (['هل الـAI هيستبدل الـTester؟', 'شاشة ليا وشاشة للـAI', 'الـAI مش بيستبدلنا.. بيسرّعنا'],
        'الـAI بقى بيعمل Manual Testing وTest Cases وDemo Videos، بس لحد دلوقتي هو Tool بتسرّع الشغل مش بديل.',
        '#AI #SoftwareTesting #QA', 'الـAI ساعدك ولا خوّفك؟'),
    3: (['هل الـTesting شغل ممل؟', 'قالولي المجال ده ممل.. ملقيتش ملل', 'الـTesting مش روتين'],
        'الملل على حسبك: هتنفّذ التاسك وخلاص، ولا هتكتشف الـEnvironment وتتعلم Tools جديدة؟',
        '#SoftwareTesting #QA #Career', 'شغلك ممل ولا إنت اللي بتخليه ممل؟'),
    4: (['ننزّل الـApp من غير Testing والناس تبلّغ؟', 'Bug في الـRefund = فلوس حقيقية', 'سمعة الشركة أغلى من الـTesting'],
        'سيب الناس تلاقي الـBugs؟ ممكن.. إلا في الفلوس والـPayments. وكمان سمعة الشركة: اللي يلاقي Bugs مش هيديلك فرصة تاني.',
        '#SoftwareTesting #Production #QA', 'مرة Application ضيّع عليك فلوس؟'),
    5: (['لازم تكون خريج حاسبات عشان تبقى Tester؟', 'مش خريج Computer Science؟ عادي', 'المهم تذاكر وتفهم'],
        'ناس كتير شغالة Testing وDevelopment ومش خريجين Computer Science.. المهم تذاكر وتفهم المنهج.',
        '#SoftwareTesting #ComputerScience #Career', 'إنت خريج إيه؟'),
    6: (['الـAI خد شغل الـJunior؟', 'الطلب على الـTesters لسه موجود؟', 'Seniors كتير.. والـJunior بقى مطلوب منه أكتر'],
        'الطلب لسه كتير على الـSeniors، بس الـJunior بقى مطلوب منه تفاصيل أكتر، لإن الحاجات البسيطة الـAI بيعملها.',
        '#AI #Career #SoftwareTesting', 'إنت Junior ولا Senior؟'),
    7: (['شهادة ISTQB مهمة ولا لأ؟', 'أنا مخدتش ولا شهادة.. بس اتسألت عليها', 'ISTQB Foundation Level'],
        'الـISTQB هي منهج التستنج: ذاكرها في كل الأحوال، والامتحان على حسب الشركة. وفي كل Interview بيتسأل عليها.',
        '#ISTQB #SoftwareTesting #QA', 'خدت ISTQB؟'),
    8: (['الـTester لازم يكون جوكر', 'Business وDevelopers وDesign وDatabase', 'مهارات الـTester'],
        'الـTester بيكلّم الـBusiness، ويهندل الـDevelopers، وعنده عين للـDesign، وفاهم Frontend وBackend وDatabase.',
        '#SoftwareTesting #SoftSkills #QA', 'إنهي مهارة فيهم ناقصاك؟'),
    9: (['يعني إيه QC؟ ببساطة', 'الـSoftware Testing في دقيقة', 'شغال صح؟ وزي ما اتطلب؟'],
        'اختبار أي Software من ناحيتين: فيه مشاكل؟ وبيعمل الـRequirements اللي اتطلبت؟ وكمان سريع وآمن.',
        '#QC #SoftwareTesting #QA', 'كنت تعرف الشغلانة دي قبل كده؟'),
    10: (['تبدأ Testing منين؟', 'ISTQB → Manual → Automation', 'أول Script في حياتك بقى سهل'],
         'افهم الـSoftware، ذاكر ISTQB Foundation، طلّع Bugs بإيدك واعمل Report، وبعدين Automation بأي لغة.',
         '#SoftwareTesting #ISTQB #Automation', 'إنت في أنهي خطوة فيهم؟'),
    11: (['Manual ولا Automation؟', 'Login Page واحدة.. وتست بطريقتين', 'ليه الـAutomation؟'],
         'الـManual: تجرب كل الاحتمالات بإيدك وبعينك. الـAutomation: كود يكرر نفس التست كل مرة ويطلّع Report.',
         '#Automation #ManualTesting #QA', 'بتحب Manual ولا Automation؟'),
    12: (['الـAI قلّل الـBugs؟', 'الـAI معندوش عقل بشري', 'لسه الـTester محتاج؟'],
         'علي شايف الـBugs زي ما هي، وأيمن شايفها قلّت شوية.. بس الـAI لسه موصلش لأدق التفاصيل.',
         '#AI #Bugs #SoftwareTesting', 'إنت شايف الـBugs قلّت؟'),
    13: (['حد بيدخل Testing عن شغف؟', 'جرّب كل حاجة.. واختار Testing', 'من Flutter للـTesting'],
         'أيمن جرّب Mobile وFrontend وBackend وGraphic Design، واختار Testing عن شغف.. مش صدفة.',
         '#SoftwareTesting #Career #Passion', 'إنت اخترت مجالك عن شغف؟'),
    14: (['يعني إيه API Testing؟', 'Postman بدل الـBrowser', 'Automation وSecurity وPerformance'],
         'بدل ما تفتح الـBrowser، بتكلّم الـAPI نفسها على Postman. وتقدر تعملها Automation، وفيه كمان Security وPerformance.',
         '#API #Postman #SoftwareTesting', 'جرّبت Postman قبل كده؟'),
    15: (['نصيحة لأي حد خايف من الـAI', 'الـAI أمر واقع', 'واكب وذاكر بالطرق الجديدة'],
         'مش هنرجع لعصر ما قبل الـAI: ذاكر، واجتهد، وواكب التطور.',
         '#AI #Career #نصيحة', 'إيه اللي بتذاكره دلوقتي؟'),
    16: (['إزاي تعرف الصح من الغلط؟', 'Requirements + خبرة', 'حاجات الـClient مطلبهاش'],
         'الـTester بيقيس على الـRequirements المكتوبة، وعلى خبرته في حاجات الـClient نفسه مطلبهاش.',
         '#Requirements #SoftwareTesting #QA', 'إيه أغرب Requirement شفته؟'),
    17: (['الـTester بيعرف الـBug فين قبل ما يدوّر', 'تتوقّع الـBug', 'المعرفة بتختصر الطريق'],
         'لما تبقى فاهم الحاجة مبنية إزاي، بتعرف الـBug هتطلع فين وتروح عليها على طول.',
         '#Bugs #SoftwareTesting #QA', 'حصل معاك قبل كده؟'),
}

for n, sh in SHORTS.items():
    v = OUT / f"{n:02d}_{sh['slug']}.mp4"
    if not v.exists():
        continue
    titles, summary, tags, pin = META[sh['idea']]
    txt = (f"العناوين (اختار واحد):\n" + '\n'.join(f'{i + 1}. {t}' for i, t in enumerate(titles)) +
           f"\n\nالوصف:\n{titles[0]}\n{summary}\n\nمن أول حلقة في نسخة حاسبات من برنامج انت بتشتغل ايه، مع أيمن إسماعيل (Senior Software QA Engineer).\n"
           f"الحلقة كاملة على يوتيوب: {LINK}\n\n{tags} #انت_بتشتغل_ايه #AlyShorosh\n\n"
           f"الكومنت المثبّت:\n{pin}\nالحلقة كاملة هنا 👈 {LINK}\n\nترتيب النشر: {n} من {len(SHORTS)}\n")
    v.with_suffix('.txt').write_text(txt, encoding='utf-8')
    print('txt', v.with_suffix('.txt').name)
