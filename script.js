async function sendQuery() {
    try {
        const response = await fetch('selenium.php', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: query })
        });

        const data = await response.json();

        return data.result;
    } catch (error) {
        console.error("오류 발생:", error);
    }
}

async function addChat() {
    document.querySelector("input").value = '';
    const DOM = `
            <section>
                <h3>${query}</h3>
            </section>
        `;
    document.querySelector(".container").insertAdjacentHTML('beforeend', DOM);

    const res = await sendQuery(query)
    const PRE = `
        <pre>${res}</pre>
    `;
    let sections = document.querySelectorAll("section");
    sections[sections.length - 1].insertAdjacentHTML('beforeend', PRE);

    const chatContainer = document.querySelector(".container");
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

let query;

document.querySelector("input").focus();

document.querySelector("input").addEventListener("input", e => {
    query = e.target.value;
    
    if (query != '')
        document.querySelector("button").classList.remove("disabled");
    else
        document.querySelector("button").classList.add("disabled");
})

document.querySelector("input").addEventListener("keydown", e => {
    if (e.key == 'Enter') {
        document.querySelector("button").classList.add("disabled");
        addChat();
    }
})

document.querySelector("button").addEventListener("click", () => {
    document.querySelector("button").classList.add("disabled");
    addChat();
})