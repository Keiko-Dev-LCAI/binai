"""Binai multi-language support — AI replies, briefings, safety messages."""

import re
from datetime import datetime

LANG_NAMES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "pt": "Portuguese",
    "de": "German",
    "ja": "Japanese",
    "zh": "Chinese",
}

_BRIEFING_EN = {
    "greeting": "Good morning, {name}! Here's your Binai briefing.",
    "weather": "Weather: {temp}°C, {desc}.",
    "price": "LCAI price: about ${price:.4f} USD.",
    "notes": "You have {n} saved note(s).",
    "reminders": "Reminders: {items}.",
    "memories": "I remember: {items}.",
    "no_reminders": "No open reminders.",
    "no_memories": "No memories yet — tell me about yourself!",
    "default_name": "friend",
}

LANG_PACKS = {
    "en": {
        "native": "English",
        "preamble": "",
        "user_suffix": "",
        "binai_label": "BINAI:",
        "retry": (
            "Answer the following in English only. Do not use any other language.\n\n"
            "Question: {message}\n\nAnswer:"
        ),
        "briefing": _BRIEFING_EN,
        "crisis_reply": (
            "I'm really glad you reached out, and I'm sorry you're going through this. "
            "You deserve support from someone who can help right now — I'm an AI and can't "
            "keep you safe the way a real person can.\n\n"
            "Please contact one of these resources immediately:\n"
            "• 988 Suicide & Crisis Lifeline (US): call or text 988\n"
            "• Crisis Text Line: text HOME to 741741\n"
            "• Emergency: 911 (US) or your local emergency number\n\n"
            "If you can, please also reach out to someone you trust — a friend, family member, "
            "or counselor. You matter, and help is available."
        ),
        "refusal_reply": (
            "I can't help with that one — I'm not able to assist with illegal activity or "
            "anything that could seriously hurt you or someone else.\n\n"
            "Happy to help with almost anything else though — what's on your mind?"
        ),
        "aivm_busy": (
            "Still busy after waiting in line — too many testers right now. "
            "Try again in a minute. (You were not charged — Keiko pays for beta AI.)"
        ),
    },
    "es": {
        "native": "Spanish (Español)",
        "preamble": (
            "【REGLAS DE IDIOMA — MÁXIMA PRIORIDAD】\n"
            "Eres Binai en español. Debes escribir cada respuesta completamente en español.\n"
            "No uses inglés. No mezcles idiomas.\n"
            "Aunque el mensaje del usuario o las instrucciones estén en inglés, responde en español.\n"
            "---\n\n"
        ),
        "user_suffix": "\n\n(Responde en español)",
        "binai_label": "BINAI (español):",
        "retry": (
            "Responde en español solamente. No uses inglés.\n\n"
            "Pregunta: {message}\n\nRespuesta:"
        ),
        "briefing": {
            "greeting": "¡Buenos días, {name}! Aquí está tu resumen de Binai.",
            "weather": "Clima: {temp}°C, {desc}.",
            "price": "Precio de LCAI: aproximadamente ${price:.4f} USD.",
            "notes": "Tienes {n} nota(s) guardada(s).",
            "reminders": "Recordatorios: {items}.",
            "memories": "Recuerdo: {items}.",
            "no_reminders": "No hay recordatorios pendientes.",
            "no_memories": "Aún no hay recuerdos — ¡cuéntame sobre ti!",
            "default_name": "amigo",
        },
        "crisis_reply": (
            "Me alegra que hayas escrito. Siento que estés pasando por esto. "
            "Mereces apoyo de alguien que pueda ayudarte ahora — soy una IA y no puedo "
            "protegerte como una persona real.\n\n"
            "Por favor contacta uno de estos recursos de inmediato:\n"
            "• Línea 988 de crisis y suicidio (EE.UU.): llama o envía mensaje al 988\n"
            "• Crisis Text Line: envía HOME al 741741\n"
            "• Emergencias: 911 (EE.UU.) o el número local de emergencias\n\n"
            "Si puedes, habla con alguien de confianza. Importas, y hay ayuda disponible."
        ),
        "refusal_reply": (
            "No puedo ayudar con eso — no puedo asistir con actividad ilegal ni "
            "algo que pueda hacerte daño a ti o a otros.\n\n"
            "Pero con casi todo lo demás sí puedo ayudar — ¿qué tienes en mente?"
        ),
        "aivm_busy": (
            "Sigue ocupado tras esperar en cola — demasiados testers ahora. "
            "Inténtalo en un minuto. (No se te cobró — Keiko paga la IA beta.)"
        ),
    },
    "fr": {
        "native": "French (Français)",
        "preamble": (
            "【RÈGLES DE LANGUE — PRIORITÉ MAXIMALE】\n"
            "Tu es Binai en français. Tu dois écrire chaque réponse entièrement en français.\n"
            "N'utilise pas l'anglais. Ne mélange pas les langues.\n"
            "Même si le message ou les instructions sont en anglais, réponds en français.\n"
            "---\n\n"
        ),
        "user_suffix": "\n\n(Réponds en français)",
        "binai_label": "BINAI (français) :",
        "retry": (
            "Réponds en français uniquement. N'utilise pas l'anglais.\n\n"
            "Question : {message}\n\nRéponse :"
        ),
        "briefing": {
            "greeting": "Bonjour, {name} ! Voici ton briefing Binai.",
            "weather": "Météo : {temp}°C, {desc}.",
            "price": "Prix LCAI : environ ${price:.4f} USD.",
            "notes": "Tu as {n} note(s) enregistrée(s).",
            "reminders": "Rappels : {items}.",
            "memories": "Je me souviens : {items}.",
            "no_reminders": "Aucun rappel en cours.",
            "no_memories": "Pas encore de souvenirs — parle-moi de toi !",
            "default_name": "ami",
        },
        "crisis_reply": (
            "Je suis content que tu aies écrit. Je suis désolé que tu traverses cela. "
            "Tu mérites le soutien de quelqu'un qui peut t'aider maintenant — je suis une IA "
            "et je ne peux pas te protéger comme une vraie personne.\n\n"
            "Contacte immédiatement l'une de ces ressources :\n"
            "• Ligne de crise 988 (États-Unis) : appelez ou envoyez 988\n"
            "• Crisis Text Line : envoyez HOME au 741741\n"
            "• Urgences : 911 (États-Unis) ou le numéro local\n\n"
            "Si tu peux, parle à quelqu'un de confiance. Tu comptes, et de l'aide est disponible."
        ),
        "refusal_reply": (
            "Je ne peux pas aider avec ça — je ne peux pas assister une activité illégale "
            "ou quelque chose qui pourrait te blesser ou blesser quelqu'un d'autre.\n\n"
            "Mais pour presque tout le reste, je suis là — qu'as-tu en tête ?"
        ),
        "aivm_busy": (
            "Toujours occupé après attente en file — trop de testeurs. "
            "Réessaie dans une minute. (Pas de frais — Keiko paie l'IA beta.)"
        ),
    },
    "pt": {
        "native": "Portuguese (Português)",
        "preamble": (
            "【REGRAS DE IDIOMA — PRIORIDADE MÁXIMA】\n"
            "Você é o Binai em português. Deve escrever cada resposta inteiramente em português.\n"
            "Não use inglês. Não misture idiomas.\n"
            "Mesmo que a mensagem ou instruções estejam em inglês, responda em português.\n"
            "---\n\n"
        ),
        "user_suffix": "\n\n(Responda em português)",
        "binai_label": "BINAI (português):",
        "retry": (
            "Responda em português somente. Não use inglês.\n\n"
            "Pergunta: {message}\n\nResposta:"
        ),
        "briefing": {
            "greeting": "Bom dia, {name}! Aqui está seu resumo do Binai.",
            "weather": "Clima: {temp}°C, {desc}.",
            "price": "Preço do LCAI: cerca de ${price:.4f} USD.",
            "notes": "Você tem {n} nota(s) salva(s).",
            "reminders": "Lembretes: {items}.",
            "memories": "Eu lembro: {items}.",
            "no_reminders": "Nenhum lembrete pendente.",
            "no_memories": "Ainda sem memórias — me conte sobre você!",
            "default_name": "amigo",
        },
        "crisis_reply": (
            "Fico feliz que você tenha escrito. Sinto muito que esteja passando por isso. "
            "Você merece apoio de alguém que possa ajudar agora — sou uma IA e não posso "
            "protegê-lo como uma pessoa real.\n\n"
            "Entre em contato com um destes recursos imediatamente:\n"
            "• Linha 988 de crise e suicídio (EUA): ligue ou envie mensagem para 988\n"
            "• Crisis Text Line: envie HOME para 741741\n"
            "• Emergência: 911 (EUA) ou o número local\n\n"
            "Se puder, fale com alguém de confiança. Você importa, e há ajuda disponível."
        ),
        "refusal_reply": (
            "Não posso ajudar com isso — não posso auxiliar atividade ilegal nem "
            "algo que possa machucar você ou outra pessoa.\n\n"
            "Mas com quase tudo mais posso ajudar — o que você tem em mente?"
        ),
        "aivm_busy": (
            "Ainda ocupado após esperar na fila — muitos testadores. "
            "Tente em um minuto. (Você não foi cobrado — Keiko paga a IA beta.)"
        ),
    },
    "de": {
        "native": "German (Deutsch)",
        "preamble": (
            "【SPRACHREGELN — HÖCHSTE PRIORITÄT】\n"
            "Du bist Binai auf Deutsch. Du musst jede Antwort vollständig auf Deutsch schreiben.\n"
            "Verwende kein Englisch. Mische keine Sprachen.\n"
            "Auch wenn die Nachricht oder Anweisungen auf Englisch sind, antworte auf Deutsch.\n"
            "---\n\n"
        ),
        "user_suffix": "\n\n(Antworte auf Deutsch)",
        "binai_label": "BINAI (Deutsch):",
        "retry": (
            "Antworte nur auf Deutsch. Verwende kein Englisch.\n\n"
            "Frage: {message}\n\nAntwort:"
        ),
        "briefing": {
            "greeting": "Guten Morgen, {name}! Hier ist dein Binai-Briefing.",
            "weather": "Wetter: {temp}°C, {desc}.",
            "price": "LCAI-Preis: etwa ${price:.4f} USD.",
            "notes": "Du hast {n} gespeicherte Notiz(en).",
            "reminders": "Erinnerungen: {items}.",
            "memories": "Ich erinnere mich: {items}.",
            "no_reminders": "Keine offenen Erinnerungen.",
            "no_memories": "Noch keine Erinnerungen — erzähl mir von dir!",
            "default_name": "Freund",
        },
        "crisis_reply": (
            "Ich bin froh, dass du geschrieben hast. Es tut mir leid, dass du das durchmachst. "
            "Du verdienst Unterstützung von jemandem, der dir jetzt helfen kann — ich bin eine KI "
            "und kann dich nicht schützen wie eine echte Person.\n\n"
            "Bitte kontaktiere sofort eine dieser Ressourcen:\n"
            "• 988 Suizid- und Krisenhotline (USA): rufe oder schreibe 988\n"
            "• Crisis Text Line: schreibe HOME an 741741\n"
            "• Notfall: 911 (USA) oder die lokale Notrufnummer\n\n"
            "Wenn du kannst, sprich mit jemandem, dem du vertraust. Du bist wichtig."
        ),
        "refusal_reply": (
            "Damit kann ich nicht helfen — ich kann keine illegale Aktivität unterstützen "
            "oder etwas, das dir oder anderen ernsthaft schaden könnte.\n\n"
            "Bei fast allem anderen helfe ich gern — was beschäftigt dich?"
        ),
        "aivm_busy": (
            "Nach Wartezeit immer noch ausgelastet — zu viele Tester. "
            "Bitte in einer Minute erneut versuchen. (Keine Kosten für dich — Keiko zahlt.)"
        ),
    },
    "ja": {
        "native": "Japanese (日本語)",
        "preamble": (
            "【言語ルール — 最優先】\n"
            "あなたは日本語の Binai です。すべての返信を日本語で書いてください。\n"
            "英語は使わないでください。言語を混ぜないでください。\n"
            "ユーザーのメッセージや指示が英語でも、日本語で答えてください。\n"
            "---\n\n"
        ),
        "user_suffix": "\n\n（日本語で答えてください）",
        "binai_label": "BINAI（日本語）:",
        "retry": (
            "日本語だけで答えてください。英語は使わないでください。\n\n"
            "質問：{message}\n\n回答："
        ),
        "briefing": {
            "greeting": "おはよう、{name}さん！Binai のブリーフィングです。",
            "weather": "天気：{temp}°C、{desc}。",
            "price": "LCAI 価格：約 ${price:.4f} USD。",
            "notes": "保存されたメモが {n} 件あります。",
            "reminders": "リマインダー：{items}。",
            "memories": "覚えていること：{items}。",
            "no_reminders": "未完了のリマインダーはありません。",
            "no_memories": "まだ記憶がありません — あなたのことを教えてください！",
            "default_name": "友達",
        },
        "crisis_reply": (
            "連絡してくれてうれしいです。つらい状況ですね。今すぐ助けてくれる人の "
            "サポートが必要です — 私はAIなので、本当の人のように守ることはできません。\n\n"
            "すぐに次のリソースに連絡してください：\n"
            "• 米国 988 自殺・危機ホットライン：988 に電話またはメッセージ\n"
            "• Crisis Text Line：741741 に HOME と送信\n"
            "• 緊急時：911（米国）または地域の緊急番号\n\n"
            "信頼できる人にも話してみてください。あなたは大切な存在です。"
        ),
        "refusal_reply": (
            "それについてはお手伝いできません — 違法行為や、あなたや他人に "
            "深刻な危害を与える可能性があることはサポートできません。\n\n"
            "それ以外のことならほとんど何でもお手伝いします — 何かありますか？"
        ),
        "aivm_busy": (
            "順番待ちしてもまだ混雑しています。1分後にもう一度お試しください。"
            "（料金はかかりません — Keiko がベータ AI を支払います）"
        ),
    },
    "zh": {
        "native": "Simplified Chinese (简体中文)",
        "preamble": (
            "【语言规则 — 最高优先级，不可违反】\n"
            "你是 Binai 中文助手。你必须用简体中文写每一条回复。\n"
            "不要用英文回复。不要用中英混杂。\n"
            "即使用户消息或系统说明是英文，你的回答仍必须是简体中文。\n"
            "---\n\n"
        ),
        "user_suffix": "\n\n（请用简体中文回答）",
        "binai_label": "BINAI（简体中文）:",
        "retry": (
            "请用简体中文回答以下问题。只使用中文，不要英文。\n\n"
            "问题：{message}\n\n"
            "回答："
        ),
        "briefing": {
            "greeting": "早上好，{name}！这是你的 Binai 简报。",
            "weather": "天气：{temp}°C，{desc}。",
            "price": "LCAI 价格：约 ${price:.4f} 美元。",
            "notes": "你有 {n} 条已保存笔记。",
            "reminders": "提醒：{items}。",
            "memories": "我记得：{items}。",
            "no_reminders": "暂无待办提醒。",
            "no_memories": "暂无记忆 — 和我聊聊你自己吧！",
            "default_name": "朋友",
        },
        "crisis_reply": (
            "很高兴你联系我。很抱歉你正在经历这些。你现在需要能真正帮助你的人 — "
            "我是 AI，无法像真人一样保护你。\n\n"
            "请立即联系以下资源：\n"
            "• 美国 988 自杀与危机热线：拨打或发短信 988\n"
            "• Crisis Text Line：发短信 HOME 到 741741\n"
            "• 紧急求助：911（美国）或当地急救电话\n\n"
            "如果可以，也请告诉你信任的人。你很重要，帮助是可以获得的。"
        ),
        "refusal_reply": (
            "这个我无法帮助 — 我不能协助违法活动，或可能严重伤害你或他人的事情。\n\n"
            "但几乎所有其他事情我都可以帮忙 — 你想聊什么？"
        ),
        "aivm_busy": (
            "排队等了一阵子还是太忙了 — 测试人数较多。"
            "请一分钟后再试。（你不会被收费 — Keiko 支付测试版 AI。）"
        ),
    },
}


def aivm_busy_message(lang):
    return lang_pack(lang).get("aivm_busy", LANG_PACKS["en"]["aivm_busy"])


_AIVM_INFRA_PATTERNS = (
    "temporarily unavailable",
    "network or aivm issue",
    "replacement transaction underpriced",
    "-32000",
    "aivm timed out",
    "aivm job failed",
    "createsession reverted",
    "submitjob reverted",
    "no response from aivm",
    "error:",
)

_BAD_AI_PATTERNS = (
    "lightnode sdk",
    "private key",
    "seed phrase",
    "私钥",
    "助记词",
    "here's a response in simplified chinese",
    "here is a response in simplified chinese",
    "response in simplified chinese:",
)

_BOOKING_PATTERNS = (
    re.compile(r"预约|挂号|就诊|看医生"),
    re.compile(r"book\s+(?:a\s+)?(?:doctor|medical|appointment)", re.I),
)

_BOOKING_REPLIES = {
    "en": (
        "I can't book doctor appointments or make calls for you yet — that isn't built into Binai.\n\n"
        "What you can do:\n"
        "1. Call or use your hospital's app/website yourself\n"
        "2. Add a reminder in Binai for Tuesday 3:00 PM\n"
        "3. Ask me to draft what to say when you call\n\n"
        "Want help with a reminder or a short script to say?"
    ),
    "zh": (
        "我还不能帮你直接预约医生或打电话——这个功能还没上线。\n\n"
        "你可以：\n"
        "1. 自己打医院电话或用医院 App/网站预约\n"
        "2. 在 Binai「提醒」里记下下周二下午 3 点\n"
        "3. 让我帮你写一段预约时要说的话\n\n"
        "需要我帮你设提醒或写预约话术吗？"
    ),
    "es": (
        "Todavía no puedo reservar citas médicas ni hacer llamadas por ti.\n\n"
        "Puedes:\n"
        "1. Llamar o usar la app/web del hospital\n"
        "2. Crear un recordatorio en Binai\n"
        "3. Pedirme un guion corto para la llamada\n\n"
        "¿Quieres ayuda con un recordatorio o un guion?"
    ),
    "fr": (
        "Je ne peux pas encore prendre de rendez-vous médicaux ni passer d'appels pour toi.\n\n"
        "Tu peux :\n"
        "1. Appeler ou utiliser l'app/site de l'hôpital\n"
        "2. Ajouter un rappel dans Binai\n"
        "3. Me demander un court script pour l'appel\n\n"
        "Tu veux de l'aide pour un rappel ou un script ?"
    ),
    "pt": (
        "Ainda não posso marcar consultas médicas nem fazer ligações por você.\n\n"
        "Você pode:\n"
        "1. Ligar ou usar o app/site do hospital\n"
        "2. Criar um lembrete no Binai\n"
        "3. Pedir um roteiro curto para a ligação\n\n"
        "Quer ajuda com um lembrete ou roteiro?"
    ),
    "de": (
        "Ich kann noch keine Arzttermine buchen oder Anrufe für dich machen.\n\n"
        "Du kannst:\n"
        "1. Selbst anrufen oder die Klinik-App/Website nutzen\n"
        "2. Eine Erinnerung in Binai anlegen\n"
        "3. Mich um einen kurzen Anruf-Text bitten\n\n"
        "Soll ich bei einer Erinnerung oder einem Text helfen?"
    ),
    "ja": (
        "まだ診察の予約や電話代行はできません。\n\n"
        "できること：\n"
        "1. 自分で病院に電話、またはアプリ/サイトで予約\n"
        "2. Binai のリマインダーに登録\n"
        "3. 電話で言う内容の下書きをお手伝い\n\n"
        "リマインダーや下書きを手伝いましょうか？"
    ),
}


def is_aivm_infra_failure(text):
    body = (text or "").strip().lower()
    if not body:
        return True
    return any(p in body for p in _AIVM_INFRA_PATTERNS)


def is_bad_ai_reply(text):
    body = (text or "").strip().lower()
    if not body:
        return True
    return any(p in body for p in _BAD_AI_PATTERNS)


def is_booking_request(message):
    msg = (message or "").strip()
    if not msg:
        return False
    return any(p.search(msg) for p in _BOOKING_PATTERNS)


def booking_reply(lang):
    return _BOOKING_REPLIES.get(lang, _BOOKING_REPLIES["en"])


_BRIEF_GREETING_PATTERNS = [
    re.compile(
        r"^(gm|gn|good\s+morning|good\s+night|good\s+evening|good\s+afternoon|"
        r"hey|hi|hello|yo|sup|what'?s\s+up|morning|afternoon|evening)[\s!.?💜☀️🌅]*$",
        re.I,
    ),
    re.compile(r"^(thanks|thank\s+you|thx|ty|cheers)[\s!.?]*$", re.I),
    re.compile(r"happy\s+[\w\s]+\s*day", re.I),
    re.compile(r"^(ok|okay|cool|nice|great|got\s+it|sounds\s+good)[\s!.?]*$", re.I),
]

_TIME_PATTERNS = [
    re.compile(r"\bwhat\s+time\b", re.I),
    re.compile(r"\bwhat'?s\s+the\s+time\b", re.I),
    re.compile(r"\bcurrent\s+time\b", re.I),
    re.compile(r"\bwhat\s+time\s+is\s+it\b", re.I),
]

_BRIEF_SKIP_PATTERNS = [
    re.compile(r"\bremember\b", re.I),
    re.compile(r"\b(plan|explain|help\s+me|tell\s+me\s+about|write|draft|list)\b", re.I),
]

REPLY_DEPTHS = ("short", "balanced", "chatty")

_BRIEF_INTENT_INSTRUCTIONS = {
    "short": {
        "en": (
            "THIS MESSAGE IS SHORT/CASUAL. Reply in 1–2 sentences max. "
            "No follow-up questions. No paragraphs."
        ),
        "zh": "这是简短消息。最多 1–2 句话。不要追问。",
    },
    "balanced": {
        "en": (
            "THIS MESSAGE IS SHORT/CASUAL. Keep it to 2–3 sentences. "
            "One brief warm line is fine; avoid long paragraphs."
        ),
        "zh": "这是简短消息。2–3 句话即可。可以温暖，但不要长篇。",
    },
    "chatty": {
        "en": (
            "THIS MESSAGE IS SHORT but the user likes conversation. "
            "You may ask one natural follow-up question. Stay under 5 sentences."
        ),
        "zh": "消息较短，但用户喜欢聊天。可以问一个自然的追问。不超过 5 句。",
    },
}

_REPLY_DEPTH_INSTRUCTIONS = {
    "short": {
        "en": (
            "USER REPLY LENGTH: SHORT. Default 1–2 sentences. "
            "Greetings (GM, hi): one line back — no follow-up questions. "
            "Simple facts: one direct answer."
        ),
        "zh": "回复长度：简短。默认 1–2 句。问候一句带过，不要追问。",
    },
    "balanced": {
        "en": (
            "USER REPLY LENGTH: BALANCED (default). Usually 2–4 sentences. "
            "Greetings: warm but brief. Follow-ups OK when the topic invites it. "
            "Go longer only when they ask for plans, advice, or detail."
        ),
        "zh": "回复长度：均衡。通常 2–4 句。问候温暖但简短。需要时可追问。",
    },
    "chatty": {
        "en": (
            "USER REPLY LENGTH: CHATTY. Be conversational — questions welcome. "
            "Engage naturally; up to ~5 sentences on casual chat. "
            "Still skip essays on simple GM/hi unless they clearly want to talk."
        ),
        "zh": "回复长度：健谈。可以对话、可以追问。自然聊天，约 5 句以内。",
    },
}

_OPEN_SHORT_PAT = re.compile(
    r"\b(bored|lonely|sad|upset|anxious|stressed|depressed|help|why|feel|thinking|miss)\b",
    re.I,
)

_QUICK_GREETINGS = {
    "en": {
        "gm": "Good morning{name}! ☀️",
        "gn": "Good night{name}. 💜",
        "default": "Hey{name}! 💜",
        "holiday": "Happy {holiday}{name}! 💜",
        "thanks": "You're welcome{name}! 💜",
    },
    "zh": {
        "gm": "早上好{name}！☀️",
        "gn": "晚安{name}。💜",
        "default": "你好{name}！💜",
        "holiday": "{holiday}快乐{name}！💜",
        "thanks": "不客气{name}！💜",
    },
    "es": {
        "gm": "¡Buenos días{name}! ☀️",
        "gn": "Buenas noches{name}. 💜",
        "default": "¡Hola{name}! 💜",
        "holiday": "¡Feliz {holiday}{name}! 💜",
        "thanks": "¡De nada{name}! 💜",
    },
    "fr": {
        "gm": "Bonjour{name} ! ☀️",
        "gn": "Bonne nuit{name}. 💜",
        "default": "Salut{name} ! 💜",
        "holiday": "Joyeux/Joyeuse {holiday}{name} ! 💜",
        "thanks": "Avec plaisir{name} ! 💜",
    },
    "pt": {
        "gm": "Bom dia{name}! ☀️",
        "gn": "Boa noite{name}. 💜",
        "default": "Olá{name}! 💜",
        "holiday": "Feliz {holiday}{name}! 💜",
        "thanks": "De nada{name}! 💜",
    },
    "de": {
        "gm": "Guten Morgen{name}! ☀️",
        "gn": "Gute Nacht{name}. 💜",
        "default": "Hallo{name}! 💜",
        "holiday": "Frohen/Frohe {holiday}{name}! 💜",
        "thanks": "Gern geschehen{name}! 💜",
    },
    "ja": {
        "gm": "おはよう{name}！☀️",
        "gn": "おやすみ{name}。💜",
        "default": "こんにちは{name}！💜",
        "holiday": "{holiday}おめでとう{name}！💜",
        "thanks": "どういたしまして{name}！💜",
    },
}

_HOLIDAY_PHRASES = {
    "en": {"fathers": "Father's Day", "mothers": "Mother's Day", "birthday": "birthday"},
    "zh": {"fathers": "父亲节", "mothers": "母亲节", "birthday": "生日"},
}


def resolve_reply_depth(prefs):
    prefs = prefs or {}
    depth = prefs.get("reply_depth")
    if depth in REPLY_DEPTHS:
        return depth
    personality = prefs.get("personality") or "warm"
    if personality in ("direct", "professional"):
        return "short"
    if personality == "playful":
        return "chatty"
    return "balanced"


def reply_depth_instruction(depth, lang):
    pack = _REPLY_DEPTH_INSTRUCTIONS.get(depth, _REPLY_DEPTH_INSTRUCTIONS["balanced"])
    return pack.get(lang, pack["en"])


def is_brief_intent(message):
    msg = (message or "").strip()
    if not msg or len(msg) > 140:
        return False
    if any(p.search(msg) for p in _BRIEF_SKIP_PATTERNS):
        return False
    if any(p.search(msg) for p in _TIME_PATTERNS):
        return True
    if any(p.search(msg) for p in _BRIEF_GREETING_PATTERNS):
        return True
    words = msg.split()
    if len(words) <= 4 and "?" not in msg:
        if _OPEN_SHORT_PAT.search(msg):
            return False
        return True
    if "?" in msg and len(words) <= 10:
        low = msg.lower()
        if any(k in low for k in ("time", "date", "weather", "temperature")):
            return True
    return False


def brief_intent_instruction(lang, depth="balanced"):
    pack = _BRIEF_INTENT_INSTRUCTIONS.get(depth, _BRIEF_INTENT_INSTRUCTIONS["balanced"])
    return pack.get(lang, pack["en"])


def _name_suffix(name, lang):
    n = (name or "").strip()
    if not n:
        return ""
    if lang == "zh":
        return f"，{n}"
    return f", {n}"


def _format_quick(template, lang, name="", **kwargs):
    pack = _QUICK_GREETINGS.get(lang, _QUICK_GREETINGS["en"])
    tpl = pack.get(template, pack["default"])
    return tpl.format(name=_name_suffix(name, lang), **kwargs)


def _greeting_kind(message):
    msg = (message or "").strip().lower()
    if re.search(r"\b(gm|good\s+morning|morning)\b", msg):
        return "gm"
    if re.search(r"\b(gn|good\s+night)\b", msg):
        return "gn"
    if re.search(r"\b(thanks|thank\s+you|thx|ty)\b", msg):
        return "thanks"
    if re.search(r"happy\s+(\w+)\s*day", msg, re.I):
        m = re.search(r"happy\s+(\w+)\s*day", msg, re.I)
        return ("holiday", m.group(1) if m else "day")
    return "default"


def quick_time_reply(lang):
    now = datetime.now()
    clock = now.strftime("%-I:%M %p") if hasattr(now, "strftime") else now.strftime("%I:%M %p")
    clock = clock.lstrip("0")
    templates = {
        "en": f"It's {clock} on my end — check your phone for local time.",
        "zh": f"我这边是 {clock} — 请看手机上的本地时间。",
        "es": f"Aquí son las {clock} — mira la hora local en tu teléfono.",
        "fr": f"Il est {clock} ici — vérifie l'heure locale sur ton téléphone.",
        "pt": f"Aqui são {clock} — confira a hora local no seu celular.",
        "de": f"Hier ist es {clock} — schau auf deinem Handy nach der lokalen Zeit.",
        "ja": f"こちらは {clock} です — お使いの端末で現地時間を確認してください。",
    }
    return templates.get(lang, templates["en"])


def quick_chat_reply(message, lang, name="", depth="balanced"):
    msg = (message or "").strip()
    if not msg:
        return None
    if any(p.search(msg) for p in _TIME_PATTERNS):
        return quick_time_reply(lang)
    if depth != "short":
        return None
    if not is_brief_intent(msg):
        return None
    kind = _greeting_kind(msg)
    if kind == "thanks":
        return _format_quick("thanks", lang, name)
    if isinstance(kind, tuple) and kind[0] == "holiday":
        holiday_key = kind[1].lower()
        if "father" in holiday_key:
            h = _HOLIDAY_PHRASES.get(lang, _HOLIDAY_PHRASES["en"]).get("fathers", "day")
        elif "mother" in holiday_key:
            h = _HOLIDAY_PHRASES.get(lang, _HOLIDAY_PHRASES["en"]).get("mothers", "day")
        else:
            h = holiday_key
        return _format_quick("holiday", lang, name, holiday=h)
    if kind in ("gm", "gn"):
        return _format_quick(kind, lang, name)
    if len(msg.split()) <= 6:
        return _format_quick("default", lang, name)
    return None


def _split_sentences(text):
    body = (text or "").strip()
    if not body:
        return []
    parts = re.split(r"(?<=[.!?。！？])\s+", body)
    return [p.strip() for p in parts if p.strip()]


def enforce_brief_reply(reply, message, depth="balanced"):
    if depth == "chatty" or not is_brief_intent(message):
        return (reply or "").strip()
    limits = {"short": 2, "balanced": 4, "chatty": 99}
    max_sents = limits.get(depth, 4)
    sents = _split_sentences(reply)
    if len(sents) <= max_sents:
        return (reply or "").strip()
    return " ".join(sents[:max_sents]).strip()


LANG_MARKERS = {
    "en": re.compile(
        r"\b(the|and|you|your|is|are|was|were|can|will|would|should|have|has|"
        r"this|that|with|for|not|but|what|how|about|please|thank)\b",
        re.I,
    ),
    "es": re.compile(
        r"\b(el|la|los|las|de|que|es|en|un|una|por|con|para|no|sí|como|más|pero|"
        r"hola|gracias|puedo|está|tengo)\b",
        re.I,
    ),
    "fr": re.compile(
        r"\b(le|la|les|de|des|un|une|est|en|que|pour|pas|avec|vous|nous|dans|sur|"
        r"ce|cette|bonjour|merci|comment|mais)\b",
        re.I,
    ),
    "pt": re.compile(
        r"\b(o|a|os|as|de|que|é|em|um|uma|por|com|para|não|mas|como|você|"
        r"obrigado|olá|está|tenho)\b",
        re.I,
    ),
    "de": re.compile(
        r"\b(der|die|das|den|dem|ein|eine|ist|sind|und|nicht|mit|für|auf|"
        r"auch|ich|Sie|sie|haben|danke|hallo)\b",
        re.I,
    ),
}

_DETECT_PATTERNS = [
    ("zh", re.compile(r"[\u4e00-\u9fff]")),
    ("ja", re.compile(r"[\u3040-\u30ff]")),
    ("de", re.compile(r"[äöüßÄÖÜ]", re.I)),
    ("es", re.compile(r"[áéíóúñ¿¡]", re.I)),
    ("fr", re.compile(r"[àâçéèêëïîôùûüœæ]", re.I)),
    ("pt", re.compile(r"[ãõ]", re.I)),
]


def lang_pack(lang):
    return LANG_PACKS.get(lang, LANG_PACKS["en"])


def briefing_strings(lang):
    return lang_pack(lang)["briefing"]


def detect_message_lang(message):
    if not message:
        return None
    scores = {}
    for code, pat in _DETECT_PATTERNS:
        hits = len(pat.findall(message))
        if hits:
            scores[code] = hits
    if not scores:
        return None
    return max(scores, key=scores.get)


def resolve_lang(wallet_get_profile, override=None, user_message=None):
    if override and override in LANG_NAMES:
        return override
    detected = detect_message_lang(user_message)
    if detected:
        return detected
    prof = wallet_get_profile() or {}
    return prof.get("language") or "en"


def language_instruction_for(lang):
    native = lang_pack(lang)["native"]
    return (
        f"CRITICAL — The user's preferred language is {native}. "
        f"You MUST write every reply entirely in {native}. "
        "Do not switch languages unless the user clearly writes in another language first."
    )


def language_preamble(lang):
    return lang_pack(lang)["preamble"]


def prompt_user_suffix(lang):
    return lang_pack(lang)["user_suffix"]


def prompt_binai_label(lang):
    return lang_pack(lang)["binai_label"]


def retry_prompt(lang, message):
    return lang_pack(lang)["retry"].format(message=message)


def localized_safety_reply(category, lang):
    pack = lang_pack(lang)
    if category == "crisis":
        return pack["crisis_reply"]
    return pack["refusal_reply"]


def _script_score(text, lang):
    if lang == "zh":
        return len(re.findall(r"[\u4e00-\u9fff]", text))
    if lang == "ja":
        return len(re.findall(r"[\u3040-\u30ff\u4e00-\u9fff]", text))
    pat = LANG_MARKERS.get(lang)
    if pat:
        return len(pat.findall(text))
    return 0


def reply_is_wrong_language(text, lang):
    if lang == "en":
        return False
    body = (text or "").strip()
    if len(body) < 12:
        return False
    target_score = _script_score(body, lang)
    en_score = _script_score(body, "en")
    if lang in ("zh", "ja"):
        if target_score >= 8:
            return False
        return en_score >= 4 or (target_score < 3 and len(body) > 20)
    if target_score >= 3:
        return False
    return en_score >= 5


# ── Assistant name, friend mode, Smart UX strings ─────────────────────────────

def resolve_assistant_name(prefs):
    prefs = prefs or {}
    name = (prefs.get("assistant_name") or "Binai").strip()
    return (name[:20] if name else "Binai")


_CATCH_UP = {
    "en": {
        "greeting": "Hey {name} — here's what you might have missed 💜",
        "reminders": "📌 Reminders: {items}",
        "notes": "📝 Notes: {n} saved",
        "memories": "🧠 I remember: {items}",
        "price": "💰 LCAI ≈ ${price:.4f} USD",
        "all_clear": "You're all caught up — nothing urgent. I'm here if you want to chat.",
        "default_name": "friend",
    },
    "zh": {
        "greeting": "嘿 {name} — 帮你捋一下你可能错过的 💜",
        "reminders": "📌 提醒：{items}",
        "notes": "📝 笔记：{n} 条",
        "memories": "🧠 我记得：{items}",
        "price": "💰 LCAI ≈ ${price:.4f} 美元",
        "all_clear": "都还好，没有紧急的事。想聊随时找我。",
        "default_name": "朋友",
    },
}


def catch_up_strings(lang):
    return _CATCH_UP.get(lang, _CATCH_UP["en"])


_FRIEND_MODE = {
    "en": (
        "FRIEND MODE (on): Talk like a close, trusted friend — not a corporate assistant. "
        "Use natural reactions (oh, hmm, honestly…). Contractions welcome. "
        "When they ask your opinion (outfit, message tone, life stuff): be warm, specific, and kind. "
        "Never body-shame. For appearance questions, comment on fit, color, style, occasion — "
        "address how they feel, not cruel 'truth.' "
        "If they want hype vs honesty, read the room or ask once."
    ),
    "zh": (
        "朋友模式（开）：像亲密好友说话，不要客服腔。自然、有温度。 "
        "意见类问题（穿搭、好不好看、消息措辞）：具体、友善，不人身攻击。 "
        "不说伤人的话；多聊版型、颜色、场合和自信。"
    ),
}


def friend_mode_instruction(lang, enabled):
    if not enabled:
        return ""
    return _FRIEND_MODE.get(lang, _FRIEND_MODE["en"])


_APPEARANCE_OPINION = {
    "en": (
        "They may want a friend's opinion (outfit, photo, how they look). "
        "Be supportive and specific. Never say they look fat. "
        "Focus on what works; ask how they feel in it. Photos not supported yet — "
        "still help with words and confidence if they describe the outfit."
    ),
    "zh": (
        "用户可能在征求朋友式意见（穿搭、照片、好不好看）。 "
        "友善、具体，不说伤人的话。照片功能尚未接入 — 仍可根据描述给建议。"
    ),
}

_OPINION_PAT = re.compile(
    r"(what do you think|do i look|how do i look|does this (look|sound)|"
    r"outfit|dress|fat|too (big|small|much)|flattering|"
    r"你觉得|好看吗|胖|这件|穿搭|裙子|衣服)",
    re.I,
)


def is_opinion_or_appearance(message):
    return bool(_OPINION_PAT.search(message or ""))


def appearance_opinion_instruction(lang):
    return _APPEARANCE_OPINION.get(lang, _APPEARANCE_OPINION["en"])


_REMEMBER_PAT = re.compile(
    r"\b(remember|don't forget|note that|记住|记得)\b", re.I
)


def is_remember_intent(message):
    return bool(_REMEMBER_PAT.search(message or ""))


_MEMORY_CONFIRM = {
    "en": "They may be teaching you a new fact. After answering, briefly confirm one key detail you will remember (one short line).",
    "zh": "用户可能在教你新事实。回答后可简短确认你会记住的关键一点（一句）。",
}


def memory_confirm_instruction(lang):
    return _MEMORY_CONFIRM.get(lang, _MEMORY_CONFIRM["en"])


_GENTLE_SUGGESTION = {
    "en": {
        "reminder": "{name}, you have a reminder coming up: {item} — want me to keep it on your radar?",
        "memory": "{name}, I still remember: {item}. Anything you want to do about that today?",
        "morning": "Good morning{name}! ☀️ Tap Catch Me Up if you want a quick rundown.",
        "evening": "Hey{name} — long day? I'm here if you want to vent or plan tomorrow.",
        "default_name": "friend",
    },
    "zh": {
        "reminder": "{name}，你有提醒：{item} — 需要我再帮你记着吗？",
        "memory": "{name}，我还记得：{item}。今天想聊聊这个吗？",
        "morning": "早上好{name}！☀️ 点「帮我捋一下」可以快速汇总。",
        "evening": "嘿{name} — 累了吗？想聊聊或安排明天都行。",
        "default_name": "朋友",
    },
}


def gentle_open_suggestion(lang, kind, name="", item=""):
    pack = _GENTLE_SUGGESTION.get(lang, _GENTLE_SUGGESTION["en"])
    template = pack.get(kind, "")
    if not template:
        return ""
    display = (name or "").strip()
    if kind in ("morning", "evening"):
        suffix = f", {display}" if display else ""
        return template.format(name=suffix)
    who = display or pack.get("default_name", "friend")
    if lang == "zh" and not display:
        who = "朋友"
    return template.format(name=who, item=(item or "")[:120])