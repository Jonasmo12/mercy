console.log('quizjs connected')

const url = window.location.href
console.log('url: ', url)
const quizBox = document.getElementById('quiz-box')
const scoreBox = document.getElementById('score-box')
const resultBox = document.getElementById('result-box')


$.ajax({
    type: 'GET',
    url: `${url}data`,
    success: function(response) {
        console.log(response)
        let data = response.data

        data.forEach(el => {
            for (const [question, answers] of Object.entries(el)) {
            
                quizBox.innerHTML += `
                    <hr>
                    <div class="">
                        <p>${question}</p>            
                    </div>
                    <br>
                `
                answers.forEach(answer=>{
                    quizBox.innerHTML += `
                        <div>
                            <input type="radio" class="ans" id="${question}-${answer}" name="${question}" value="${answer}">
                            <label for="${question}">${answer}</label>
                        </div>    
                    `
                })
            }
        });
    },
    error: function(error) {
        console.log(error)
    } 
})


const quizForm = document.getElementById('quiz-form');
const csrf = document.getElementsByName('csrfmiddlewaretoken');



const sendData = () => {
    const elements = [...document.getElementsByClassName('ans')];
    const data = {}
    data['csrfmiddlewaretoken'] = csrf[0].value
    elements.forEach(el=>{
        if (el.checked) {
            data[el.name] = el.value
        } else {
            if (!data[el.name]) {
                data[el.name] = null
            }
        }
    })
    
    $.ajax({
        type: "POST",
        url: `${url}save/`,
        data: data,
        success: function(response) {
            // console.log(response)
            const results = response.results
            console.log(results)
            quizForm.classList.add('not-visible') 
            

            scoreBox.innerHTML += `${response.passed ? 'Congratulations! ' : 'Oops! '} You scored ${response.score.toFixed(2)}%`

            results.forEach(res=>{
                const resultsDiv = document.createElement("div")
                for (const [question, resp] of Object.entries(res)) {
                    resultsDiv.innerHTML += question
                    const cls = ['ui', 'container']
                    resultsDiv.classList.add(...cls)

                    if (resp=="not answered") {
                        resultsDiv.innerHTML += '-not answered'
                        resultsDiv.classList.add('bg-danger')
                    } else {
                        const answer = resp['answered']
                        const correctAnswer = resp['correctAnswer']
                    }

                }
            })
        },
        error: function(error) {
            console.log(error)
        }
    })
}

quizForm.addEventListener('submit', e=>{
    e.preventDefault()

    sendData()
})