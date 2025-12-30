import streamlit as st
import time
import string
from datetime import datetime
import plotly.express as px

# -------------------------------
# Streamlit Page Config
# -------------------------------
st.set_page_config(page_title="Chat Analyzer", layout="wide")

st.title("🪄 CHAT-ANALYZER")
st.subheader("⚜️ Upload Your Files and We Do the MAGIC for You")

uploaded_file = st.file_uploader("🧛 Upload your file here (txt only)", type="txt")
placeholder = st.empty()

if uploaded_file is not None:
    # -------------------------------
    # Loading animation
    # -------------------------------
    placeholder.markdown("""
        <style>
        .blink {
            animation: blinker 1s linear infinite;
            color: white;
            font-weight: bold;
            font-size: 22px;
        }
        @keyframes blinker {
            50% { opacity: 0; }
        }
        </style>
        <div class="blink">Processing your chat...</div>
    """, unsafe_allow_html=True)

    time.sleep(2)
    placeholder.empty()
    st.success("Upload completed ✅")

    # =====================================================
    # YOUR ORIGINAL + FIXED CHAT PARSER (INTEGRATED)
    # =====================================================
    cnt = uploaded_file.read().decode("utf-8").splitlines()

    sys = []   # system messages
    usr = []   # user messages

    s = 0
    u = 0

    for i1 in cnt:
        i = i1.rstrip('\n')

        if '-' in i:
            l = i.split('-', 1)
            if len(l) < 2:
                continue

            if ':' in l[1]:
                usr.append(i)
                u = 1
                s = 0
            else:
                sys.append(i)
                s = 1
                u = 0
        else:
            if s == 1 and u == 0 and sys:
                sys[-1] += ' ' + i.strip()
            elif s == 0 and u == 1 and usr:
                usr[-1] += ' ' + i.strip()

    # -------------------------------
    # Convert to structured tuples
    # -------------------------------
    system_data = []
    user_data = []

    # USER messages
    for k in usr:
        dt_nc = k.split(' - ', 1)
        if len(dt_nc) != 2:
            continue

        d_t = dt_nc[0].split(', ', 1)
        if len(d_t) != 2:
            continue

        n_c = dt_nc[1].split(': ', 1)

        date = d_t[0]
        time_ = d_t[1]
        name = n_c[0]
        content = n_c[1] if len(n_c) == 2 else ""

        user_data.append((date, time_, name, content))

    # SYSTEM messages
    for m in sys:
        dt_c = m.split(' - ', 1)
        if len(dt_c) != 2:
            continue

        d_t = dt_c[0].split(', ', 1)
        if len(d_t) != 2:
            continue

        date = d_t[0]
        time_ = d_t[1]
        content = dt_c[1]

        system_data.append((date, time_, content))

    # -------------------------------
    # Display parsed messages
    # -------------------------------
    with st.expander("📄 User Messages"):
        st.write(user_data)

    with st.expander("⚙️ System Messages"):
        st.write(system_data)

    # =====================================================
    # MOST INTERACTIVE USER (DICTIONARY METHOD — YOUR WAY)
    # =====================================================
    d_0 = {}
    for _, _, username, _ in user_data:
        if username in d_0:
            d_0[username] += 1
        else:
            d_0[username] = 1

    max_count = 0
    top_user = ""
    for name, count in d_0.items():
        if count > max_count:
            max_count = count
            top_user = name

    # -------------------------------
    # Messages per user chart
    # -------------------------------
    users = list(d_0.keys())
    counts = list(d_0.values())

    fig = px.bar(
        x=counts,
        y=users,
        orientation="h",
        text=counts,
        color=users,
        title="📊 Messages per User",
        template="plotly_dark"
    )
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # Top user badge
    # -------------------------------
    st.subheader("👑 Most Interactive User")
    st.markdown(f"""
        <div style="background-color:#ffcc00;padding:15px;border-radius:10px;text-align:center">
            <h2>{top_user}</h2>
            <p style="font-size:18px">Messages Sent: <b>{max_count}</b></p>
            <p style="color:red;font-weight:bold;">🔥 Top Contributor</p>
        </div>
    """, unsafe_allow_html=True)

    # =====================================================
    # MOST USED WORDS (MEDIA IGNORED, NO COUNTER)
    # =====================================================
    stop_words = {
        "a","as","an","the","am","is","are","was","were","be","been","being",
        "i","me","my","mine","myself","you","your","yours",
        "he","him","his","she","her","hers","it","its",
        "we","us","our","ours","they","them","their","theirs",
        "and","or","but","nor","so","yet","because",
        "to","of","in","on","for","with","at","by","from",
        "this","that","these","those",
        "do","does","did","have","has","had",
        "can","could","will","would","should","may","might","must",
        "very","just","really","also","quite","too","enough",
        "who","whom","whose","which","what","while","when","where","why","how"
    }

    media_phrases = [
        "<media omitted>",
        "<image omitted>",
        "<video omitted>",
        "<sticker omitted>"
    ]

    message_text = ""
    for u in user_data:
        msg = u[3].lower()
        if msg not in media_phrases:
            message_text += " " + msg

    words = []
    for w in message_text.split():
        w = w.strip(string.punctuation)
        if w and w not in stop_words:
            words.append(w)

    word_dict = {}
    for w in words:
        if w in word_dict:
            word_dict[w] += 1
        else:
            word_dict[w] = 1

    max_word_count = 0
    most_used_words = []

    for word, count in word_dict.items():
        if count > max_word_count:
            max_word_count = count
            most_used_words = [word]
        elif count == max_word_count:
            most_used_words.append(word)

    # -------------------------------
    # Display most used words
    # -------------------------------
    st.subheader("📝 Most Used Word(s)")
    st.markdown("<div style='display:flex;flex-wrap:wrap'>", unsafe_allow_html=True)
    for w in most_used_words:
        st.markdown(
            f"<span style='border:2px solid #00ff99;padding:8px;margin:5px;border-radius:6px;color:#00ff99;font-size:20px'>{w}</span>",
            unsafe_allow_html=True
        )
    st.markdown("</div>", unsafe_allow_html=True)
    st.write(f"Used **{max_word_count} times**")

    # =====================================================
    # TIMELINE (NO PANDAS)
    # =====================================================
    st.subheader("🕒 Messages Over Time")

    timeline = []
    for u in user_data:
        date_str = u[0] + " " + u[1]
        try:
            dt = datetime.strptime(date_str, "%d/%m/%Y %I:%M %p")
            timeline.append(dt)
        except:
            pass

    if timeline:
        time_dict = {}
        for dt in timeline:
            hour = dt.replace(minute=0, second=0, microsecond=0)
            if hour in time_dict:
                time_dict[hour] += 1
            else:
                time_dict[hour] = 1

        times = sorted(time_dict.keys())
        values = [time_dict[t] for t in times]

        fig_time = px.line(
            x=times,
            y=values,
            markers=True,
            title="🕒 Messages Over Time",
            template="plotly_dark"
        )
        st.plotly_chart(fig_time, use_container_width=True)
    else:
        st.warning("Timeline could not be generated due to date format mismatch.")
