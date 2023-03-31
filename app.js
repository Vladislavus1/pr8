window.onload = (event) => {

    const routes = [
        {path: 'https://vladislavus1.github.io/pr8/', handler: homeHandler},
        {path: 'https://vladislavus1.github.io/pr8/index.html', handler: homeHandler},
        {path: 'https://vladislavus1.github.io/pr8/login.html', handler: loginHandler},
        {path: 'https://vladislavus1.github.io/pr8/signup.html', handler: signupHandler}
    ]

    handleUrlChange();

    function handleUrlChange () {
        const path = window.location.pathname;
        const urlPath = routes.find(route => route.path === path)

        if (urlPath) {
            urlPath.handler();
        }else {
            homeHandler();
        }
    }



function homeHandler () {
        const eventForm = document.getElementById("event-form");
        console.log(eventForm)
        const urlAddEvent = 'http://127.0.0.1:5000/create_event';
        const date = new Date().toISOString().slice(0, 10);
        getEventsByDate(date)
        .then(data => showEvents(data.data))
        logout();
        eventForm.addEventListener("submit", (event) => {
            event.preventDefault();
            console.log(event)

            sendRequestToServer(eventForm, urlAddEvent);
    })}
    function loginHandler () {
        const loginForm = document.getElementById("login-form");
        const urlLogin = 'http://127.0.0.1:5000/login.html';

        loginForm.addEventListener("submit", (event) => {
            event.preventDefault();

            sendRequestToServer(loginForm, urlLogin)
            .then(response => {if (response.isLogged) {
                    location.replace("/index.html");
                    localStorage.setItem("token", response.token);
                    console.log(localStorage.getItem("token"));
                }
    })
    })
    }

    function signupHandler () {
        const signupForm = document.getElementById("signup-form");
        const urlSignup = 'http://127.0.0.1:5000/signup';

        signupForm.addEventListener("submit", (event) => {
            event.preventDefault();

            sendRequestToServer(signupForm, urlSignup)
            .then(response => {
                if (response.isRegistered) {
                    location.replace("/login.html")
                }
            });
    })
    }




function getEventsByDate (date) {
    const apiUrlGet = `http://127.0.0.1:5000/get_events_by_date/${date}`;


    return fetch(apiUrlGet, {
        method: "GET",})
      .then(data => data.json())
      .catch(error => {
        console.error('Помилка:', error);
      });
}




    function sendRequestToServer (form, url) {

        const formData = new FormData(form);
        const data = {};

        for (const[key, value] of formData.entries()) {
            data[key] = value;
        }

        return fetch(url, {
            method: "POST",
            headers: {"Content-type": "application/json"},
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .catch(error => console.error('Помилка:', error));
    }
    function logout() {
        const btn = document.getElementById("logoutButton")
        btn.addEventListener("click", (event) => {
            localStorage.removeItem("token");
            location.replace("login.html")
        })
    }

    function showEvents (data) {
        console.log(data);
        const eventsDiv = document.getElementById("display-events");

        const singleDayEvents = document.createElement("div");
        singleDayEvents.classList.add("single-day-events");
        eventsDiv.appendChild(singleDayEvents);

        const date = JSON.parse(data[0]).date;
        console.log(data)

        if (date) {
            const dateHeader = document.createElement("h4", date, singleDayEvents);
            dateHeader.textContent = date;
            singleDayEvents.appendChild(dateHeader);
        }

        data.forEach((event) => {
                event = JSON.parse(event);

                const singleEvent = createElementAndAppendChild("div", null, singleDayEvents);

                createElementAndAppendChild("h3", event.header, singleEvent);

                createElementAndAppendChild("span", event.time, singleEvent);

                createElementAndAppendChild("span", event.description, singleEvent);
        })
    }
    function createElementAndAppendChild (tagName, content, tagAddTo) {
        const createdElement = document.createElement(tagName);
        if ( content ) { createdElement.textContent = content };
        tagAddTo.appendChild(createdElement);
        return createdElement;
    }

//    function renderEventsForFiveDays () {
//        const endDate = new Date();
//        endDate.setDate(endDate.getDate() + 5);
//        let currentDate = new Date();
//
//        while (currentDate <= endDate) {
//            const date = currentDate.toISOString();
//
//            getEventsByDate(date)
//            .then(data => showEvents(data))
//
//            currentDate.setDate(currentDate.getDate() + 1)
//        }
//    }


}


