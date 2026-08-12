async function getLogs() {
    for (let i = 1; ; i++) {
        const url = `./logs/${i}.txt`;

        try {
            const response = await fetch(url);

            if (!response.ok) break;

            logs.push(await response.text());
        } catch (e) {
            break;
        }
    }
}

let logs = [];

async function main() {
    logs = await getLogs();
    logs.forEach(log => {
        console.log(log)
    })
}