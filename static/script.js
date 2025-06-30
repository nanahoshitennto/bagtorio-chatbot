// ✅ 質問の次を表示し、選択肢を無効化＋ハイライト
function showNextQuestion(nextId, selectedText, clickedElement) {
    if (!nextId || nextId === 'qNone' || nextId === 'None') {
        nextId = 'qend';
    }

    const chatContainer = document.getElementById("chat-container");

    // 🔧 同じ質問内の選択肢すべて取得
    const parentBox = clickedElement.closest(".question-box");
    const allOptions = parentBox.querySelectorAll("a, button");

    allOptions.forEach(btn => {
        btn.classList.add("disabled");       // 他の選択肢は無効化
        btn.setAttribute("disabled", "true");
        btn.classList.remove("selected");    // 一度リセット
        btn.style.pointerEvents = "none";
    });

    // 👆 押したボタンだけ「選択済み」にする
    clickedElement.classList.add("selected");

    // ✅ 新しい質問がまだ未表示なら追加
    if (nextId !== 'qend') {
        const nextBox = document.getElementById(nextId);
        if (nextBox && !nextBox.classList.contains("show")) {
            // コメント追加
            const commentDiv = document.createElement("div");
            commentDiv.className = "chat-message chat-bot fade-in";
            commentDiv.innerHTML = `
                <div class="chat-header">
                    <img src="/static/takeoka-icon.png" alt="ロゴ" class="chat-logo">
                    <p>「${selectedText}」ですね。以下からお選びください。</p>
                </div>
            `;
            chatContainer.appendChild(commentDiv);

            nextBox.classList.add("show");
            chatContainer.appendChild(nextBox);
            nextBox.scrollIntoView({ behavior: 'smooth' });
        }
    }

    // ✅ 最後の質問（qend）の場合
    if (nextId === 'qend') {
        const restartDiv = document.createElement("div");
        restartDiv.className = "chat-message chat-bot fade-in";
        restartDiv.innerHTML = `
            <div class="chat-header">
                <img src="/static/takeoka-icon.png" alt="ロゴ" class="chat-logo">
                <p>最初からやり直す場合は <a href="#" onclick="restartChat()" style="text-decoration: underline; color: #007BFF;">こちら</a></p>
            </div>
        `;
        chatContainer.appendChild(restartDiv);
        restartDiv.scrollIntoView({ behavior: 'smooth' });
    }
}

// ✅ 最初からやり直し
function restartChat() {
    const boxes = document.querySelectorAll(".question-box, .chat-message.chat-bot");
    boxes.forEach(box => {
        if (box.classList.contains("question-box")) {
            box.classList.remove("show");
        } else {
            box.remove();
        }
    });

    // 最初の質問だけ表示
    const first = document.querySelector(".question-box");
    if (first) {
        first.classList.add("show");

        const buttons = first.querySelectorAll("a, button");
        buttons.forEach(btn => {
            btn.classList.remove("disabled", "selected");
            btn.removeAttribute("disabled");
            btn.style.pointerEvents = "";
        });

        first.scrollIntoView({ behavior: 'smooth' });
    }
}
