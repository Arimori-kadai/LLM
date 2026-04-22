document.addEventListener("DOMContentLoaded", () => {

    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");

    // FlaskサーバーのエンドポイントURL
    const API_URL = "http://127.0.0.1:5000/chat";

    sendBtn.addEventListener("click", () => {
        handleUserInput();
    });

    userInput.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            handleUserInput();
        }
    });

    function handleUserInput() {
        const messageText = userInput.value.trim();
        if (messageText !== "") {
            addMessage(messageText, "user");
            userInput.value = "";

            getLLMResponse(messageText);
        }
    }

    function addMessage(text, sender, isLoading = false) {
        const messageElement = document.createElement("div");

        // CSSクラスを設定
        messageElement.classList.add("message", sender);
        if (isLoading) {
            messageElement.classList.add("loading");
            // "loading"クラスの要素を一意に識別できるようIDを付与
            messageElement.id = "loading-message";
        }

        const pElement = document.createElement("p");
        pElement.textContent = text;

        messageElement.appendChild(pElement);
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // LLMの応答をサーバーから非同期で取得する関数 (Async/Awaitを使用)
    async function getLLMResponse(userMessage) {

        // 1. 「考え中...」のメッセージを表示
        addMessage("考え中...", "llm", true);

        try {
            // 2. Flaskサーバーにリクエストを送信
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: userMessage }),
            });

            // 3. レスポンスが正常かチェック
            if (!response.ok) {
                // サーバーからエラーが返ってきた場合 (例: 500エラー)
                throw new Error(`サーバーエラー: ${response.status}`);
            }

            // 4. レスポンスのJSONを解析
            const data = await response.json();

            // 5. 「考え中...」のメッセージを削除
            const loadingElement = document.getElementById("loading-message");
            if (loadingElement) {
                chatBox.removeChild(loadingElement);
            }

            // 6. サーバーからの応答をチャットボックスに追加
            addMessage(data.response, "llm");

        } catch (error) {
            // 7. 通信エラーが発生した場合
            console.error("通信エラー:", error);

            // 「考え中...」を削除
            const loadingElement = document.getElementById("loading-message");
            if (loadingElement) {
                chatBox.removeChild(loadingElement);
            }

            // エラーメッセージを表示
            addMessage("エラーが発生しました。サーバーに接続できません。", "llm");
        }
    }
});