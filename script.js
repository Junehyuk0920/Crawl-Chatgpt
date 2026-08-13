async function sendQuery() {
    const query = document.querySelector("input").value;
    document.querySelector("input").value = '';

    const DOM = `
            <section>
                <h2>${query}</h2>
            </section>
        `;
    document.querySelector(".container").insertAdjacentHTML('beforeend', DOM);
    const chatContainer = document.querySelector(".container");
    chatContainer.scrollTop = chatContainer.scrollHeight;

    try {
        const response = await fetch('server.php', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: query })
        });

        const data = await response.json();
        const PRE = `
            <pre>${data.result}</pre>
        `;
        let sections = document.querySelectorAll("section");
        sections[sections.length - 1].insertAdjacentHTML('beforeend', PRE);
    } catch (error) {
        console.error("오류 발생:", error);
        output.innerText = "실행 실패";
    }
}