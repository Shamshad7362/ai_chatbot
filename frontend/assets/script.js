async function sendStream() {
    const input = document.querySelector("input[name='message']");
    const box = document.getElementById("stream-output");
    const chatBox = document.getElementById("chat-box");
    const streamButton = document.querySelector(".stream-button");
    const message = input.value.trim();

    if (!message) {
        input.focus();
        return;
    }

    document.getElementById("empty-state")?.remove();
    box.textContent = "";
    box.classList.add("is-visible");
    streamButton.disabled = true;
    streamButton.textContent = "Starting...";

    try {
        const response = await fetch("/stream", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        });

        if (!response.ok) {
            throw new Error(`Request failed (${response.status})`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let answer = "";

        while (true) {
            const { value, done } = await reader.read();
            answer += decoder.decode(value || new Uint8Array(), { stream: !done });
            box.textContent = answer;
            chatBox.scrollTop = chatBox.scrollHeight;

            if (done) break;
        }

        input.value = "";
    } catch (error) {
        box.textContent = error.message || "Could not get a reply. Please try again.";
    } finally {
        streamButton.disabled = false;
        streamButton.innerHTML = '<span aria-hidden="true">◉</span> Stream';
    }
}
