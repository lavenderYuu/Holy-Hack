
function makePtner(){
    console.log(document.cookie)
    prompts = document.getElementById("Prompts").value
    gender = document.getElementById("genderTab").innerText
    fetch('http://127.0.0.1:5000/image', {
        method: 'POST',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({"prompts": gender + " with " + prompts})
    }).then(response => window.location.assign("http://127.0.0.1:5000/chatbox"))
}