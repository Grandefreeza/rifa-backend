const API = "http://localhost:5000"

function rifas() {
    fetch(API + "/rifas")
    .then(r => r.json())
    .then(d => {
        let html = "<h2>Rifas</h2>"

        d.forEach(r => {
            html += `
            <div>
                <b>${r[1]}</b>
                <button onclick="abrirRifa(${r[0]})">Abrir</button>
            </div>`
        })

        html += `
        <h3>Nova Rifa</h3>
        <input id="nome">
        <input id="qtd">
        <input id="valor">
        <input id="data" type="date">
        <button onclick="nova()">Criar</button>
        `

        conteudo.innerHTML = html
    })
}

function nova() {
    fetch(API + "/rifa", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({
            nome: nome.value,
            quantidade: qtd.value,
            valor: valor.value,
            data: data.value
        })
    }).then(() => rifas())
}

function financeiro() {
    conteudo.innerHTML = `
        <h2>Financeiro</h2>
        <button onclick="pix()">Gerar PIX</button>
        <img id="piximg">
    `
}

function pix() {
    document.getElementById("piximg").src = API + "/pix/10"
}

function relatorio() {
    conteudo.innerHTML = `
        <h2>Relatório</h2>
        <button onclick="window.print()">Imprimir</button>
        <a href="https://wa.me/?text=Veja%20minha%20rifa">Compartilhar WhatsApp</a>
    `
}