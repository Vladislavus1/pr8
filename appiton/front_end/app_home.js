window.onload = (event) => {
    console.log("http://127.0.0.1:5000/homeworkGet")
    const apiUrlGet = 'http://127.0.0.1:5000/homeworkGet';
    const apiUrlPost = 'http://127.0.0.1:5000/homeworkPost';


    fetch(apiUrlGet, {
        method: "GET",})
      .then(response => response.json())
      .then(data => {
        console.log(data); // вивести дані в консоль
      })
      .catch(error => {
        console.error('Помилка:', error);
      });


    const form = document.getElementById("event-form");

    form.addEventListener("submit", (event) => {
        event.preventDefault();

        const formData = new FormData(form);
        const data = {};

        for (const[key, value] of formData.entries()) {
            data[key] = value;
        }

        fetch(apiUrlPost, {
            method: "POST",
            headers: {"Content-type": "application/json"},
            body: JSON.stringify(data)
        })
        .then(data => console.log(data))
        .catch(error => console.error('Помилка:', error));
    })

}