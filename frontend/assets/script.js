async function sendStream() {
    const input = document.querySelector("input[name='message']").value;

    const response = await fetch("/stream", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input })
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    let text = "";
    const box = document.getElementById("stream-output");
    box.innerHTML = "";

    while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        text += decoder.decode(value);
        box.innerHTML = text;
    }
}
