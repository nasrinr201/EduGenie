const task =
    document.getElementById("task");

const inputText =
    document.getElementById("inputText");

const submitBtn =
    document.getElementById("submitBtn");

const statusBox =
    document.getElementById("status");

const result =
    document.getElementById("result");


const placeholders = {

    qa:
        "Example: What is normalization in DBMS?",

    explain:
        "Example: Explain photosynthesis in simple words.",

    quiz:
        "Paste a lesson or paragraph here to generate 3 MCQs.",

    summarize:
        "Paste your long educational passage here.",

    recommend:
        "Example: SQL"

};


task.addEventListener(
    "change",
    function () {

        inputText.placeholder =
            placeholders[task.value];

    }
);


submitBtn.addEventListener(
    "click",
    async function () {

        const text =
            inputText.value.trim();


        if (!text) {

            showStatus(
                "Please enter some content first."
            );

            return;
        }


        submitBtn.disabled = true;

        submitBtn.textContent =
            "Generating...";

        result.hidden = true;

        showStatus(
            "EduGenie is thinking..."
        );


        let endpoint;

        let payload;


        if (task.value === "qa") {

            endpoint = "/qa";

            payload = {
                question: text
            };

        }


        else if (
            task.value === "explain"
        ) {

            endpoint = "/explain";

            payload = {
                text: text
            };

        }


        else if (
            task.value === "quiz"
        ) {

            endpoint = "/quiz";

            payload = {
                text: text,
                count: 3
            };

        }


        else if (
            task.value === "summarize"
        ) {

            endpoint = "/summarize";

            payload = {
                text: text
            };

        }


        else if (
            task.value === "recommend"
        ) {

            endpoint =
                "/learn/recommendations";

            payload = {
                topic: text,
                level: "beginner"
            };

        }


        try {

            const response =
                await fetch(
                    endpoint,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(payload)
                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Something went wrong."
                );

            }


            renderResult(
                task.value,
                data
            );


            showStatus(
                "Completed successfully."
            );


        }

        catch (error) {

            showStatus(
                "Error: " +
                error.message
            );

        }


        finally {

            submitBtn.disabled = false;

            submitBtn.textContent =
                "Generate";

        }

    }
);


function showStatus(message) {

    statusBox.hidden = false;

    statusBox.textContent =
        message;
}


function renderResult(
    type,
    data
) {

    result.hidden = false;


    if (type === "quiz") {

        result.innerHTML = "";


        data.quiz.forEach(
            function (item, index) {

                const questionBlock =
                    document.createElement(
                        "div"
                    );

                questionBlock.className =
                    "quiz-question";


                const question =
                    document.createElement(
                        "strong"
                    );

                question.textContent =
                    `${index + 1}. ${item.question}`;


                questionBlock.appendChild(
                    question
                );


                item.options.forEach(
                    function (option) {

                        const label =
                            document.createElement(
                                "label"
                            );

                        label.className =
                            "quiz-option";


                        const radio =
                            document.createElement(
                                "input"
                            );

                        radio.type =
                            "radio";

                        radio.name =
                            `question-${index}`;

                        radio.value =
                            option;


                        label.appendChild(
                            radio
                        );


                        label.appendChild(
                            document.createTextNode(
                                " " + option
                            )
                        );


                        questionBlock.appendChild(
                            label
                        );

                    }
                );


                const answer =
                    document.createElement(
                        "div"
                    );

                answer.className =
                    "quiz-answer";


                answer.textContent =
                    "Correct answer: " +
                    item.answer;


                questionBlock.appendChild(
                    answer
                );


                result.appendChild(
                    questionBlock
                );

            }
        );


        return;
    }


    let key;


    if (type === "qa") {

        key = "answer";

    }

    else if (
        type === "explain"
    ) {

        key = "explanation";

    }

    else if (
        type === "summarize"
    ) {

        key = "summary";

    }

    else if (
        type === "recommend"
    ) {

        key = "learning_path";

    }


    result.textContent =
        data[key] ||
        "No result was returned.";

}