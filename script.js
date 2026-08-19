/* =====================================================
   PORTFOLIO JAVASCRIPT
   Mojesh Tripura
===================================================== */


/* =====================================================
   PAGE LOADER
===================================================== */

window.addEventListener("load", function () {

    const loader = document.getElementById("loader");

    if (loader) {

        setTimeout(function () {

            loader.style.opacity = "0";

            setTimeout(function () {

                loader.style.display = "none";

            }, 500);

        }, 800);

    }

});



/* =====================================================
   TYPING ANIMATION
===================================================== */

const typingElement = document.getElementById("typing");

if (typingElement) {

    const words = [
        "Web Developer",
        "Cybersecurity Enthusiast",
        "Problem Solver",
        "Tech Explorer"
    ];

    let wordIndex = 0;
    let charIndex = 0;
    let deleting = false;


    function typingAnimation() {

        const currentWord = words[wordIndex];


        /* TYPE */

        if (!deleting) {

            typingElement.textContent =
                currentWord.substring(
                    0,
                    charIndex + 1
                );

            charIndex++;


            /* Word completed */

            if (charIndex === currentWord.length) {

                deleting = true;

                setTimeout(
                    typingAnimation,
                    1500
                );

                return;

            }

        }


        /* DELETE */

        else {

            typingElement.textContent =
                currentWord.substring(
                    0,
                    charIndex - 1
                );

            charIndex--;


            /* Word deleted */

            if (charIndex === 0) {

                deleting = false;

                wordIndex++;

                if (wordIndex >= words.length) {

                    wordIndex = 0;

                }

            }

        }


        setTimeout(
            typingAnimation,
            deleting ? 50 : 100
        );

    }


    typingAnimation();

}



/* =====================================================
   MOBILE MENU
===================================================== */

document.addEventListener(
    "DOMContentLoaded",
    function () {


        const menuBtn =
            document.getElementById("menuBtn");


        const navLinks =
            document.getElementById("navLinks");


        /* If mobile menu doesn't exist */

        if (!menuBtn || !navLinks) {

            return;

        }


        const menuIcon =
            menuBtn.querySelector("i");



        /* =========================================
           OPEN / CLOSE MENU
        ========================================= */

        menuBtn.addEventListener(
            "click",
            function (event) {

                event.preventDefault();

                event.stopPropagation();


                navLinks.classList.toggle("active");


                const isOpen =
                    navLinks.classList.contains("active");


                if (isOpen) {


                    /* Bars → X */

                    if (menuIcon) {

                        menuIcon.classList.remove(
                            "fa-bars"
                        );

                        menuIcon.classList.add(
                            "fa-xmark"
                        );

                    }


                    menuBtn.setAttribute(
                        "aria-label",
                        "Close navigation menu"
                    );


                } else {


                    /* X → Bars */

                    if (menuIcon) {

                        menuIcon.classList.remove(
                            "fa-xmark"
                        );

                        menuIcon.classList.add(
                            "fa-bars"
                        );

                    }


                    menuBtn.setAttribute(
                        "aria-label",
                        "Open navigation menu"
                    );

                }

            }
        );



        /* =========================================
           CLOSE MENU AFTER CLICKING LINK
        ========================================= */

        const navItems =
            navLinks.querySelectorAll("a");


        navItems.forEach(
            function (link) {

                link.addEventListener(
                    "click",
                    function () {

                        navLinks.classList.remove(
                            "active"
                        );


                        if (menuIcon) {

                            menuIcon.classList.remove(
                                "fa-xmark"
                            );

                            menuIcon.classList.add(
                                "fa-bars"
                            );

                        }


                        menuBtn.setAttribute(
                            "aria-label",
                            "Open navigation menu"
                        );

                    }
                );

            }
        );



        /* =========================================
           CLOSE WHEN CLICKING OUTSIDE
        ========================================= */

        document.addEventListener(
            "click",
            function (event) {

                if (

                    !navLinks.contains(
                        event.target
                    )

                    &&

                    !menuBtn.contains(
                        event.target
                    )

                ) {


                    navLinks.classList.remove(
                        "active"
                    );


                    if (menuIcon) {

                        menuIcon.classList.remove(
                            "fa-xmark"
                        );

                        menuIcon.classList.add(
                            "fa-bars"
                        );

                    }

                }

            }
        );



        /* =========================================
           CLOSE ON DESKTOP RESIZE
        ========================================= */

        window.addEventListener(
            "resize",
            function () {

                if (window.innerWidth > 768) {

                    navLinks.classList.remove(
                        "active"
                    );


                    if (menuIcon) {

                        menuIcon.classList.remove(
                            "fa-xmark"
                        );

                        menuIcon.classList.add(
                            "fa-bars"
                        );

                    }

                }

            }
        );


    }
);



/* =====================================================
   CUSTOM CURSOR
===================================================== */

const cursor =
    document.querySelector(".cursor");

const follower =
    document.querySelector(".cursor-follower");


if (cursor && follower) {


    document.addEventListener(
        "mousemove",
        function (event) {


            cursor.style.left =
                event.clientX + "px";


            cursor.style.top =
                event.clientY + "px";


            setTimeout(
                function () {

                    follower.style.left =
                        event.clientX + "px";


                    follower.style.top =
                        event.clientY + "px";

                },
                60
            );


        }
    );

}



/* =====================================================
   SCROLL REVEAL
===================================================== */

const revealElements =
    document.querySelectorAll(
        ".section, .project-card, .skill-card, .stat"
    );


if (revealElements.length > 0) {


    const revealObserver =
        new IntersectionObserver(
            function (entries) {

                entries.forEach(
                    function (entry) {

                        if (
                            entry.isIntersecting
                        ) {

                            entry.target.classList.add(
                                "reveal"
                            );

                        }

                    }
                );

            },
            {
                threshold: 0.15
            }
        );


    revealElements.forEach(
        function (element) {

            revealObserver.observe(
                element
            );

        }
    );

}



/* =====================================================
   COUNTER ANIMATION
===================================================== */

const counters =
    document.querySelectorAll(
        "[data-target]"
    );


if (counters.length > 0) {


    const counterObserver =
        new IntersectionObserver(
            function (entries) {


                entries.forEach(
                    function (entry) {


                        if (
                            !entry.isIntersecting
                        ) {

                            return;

                        }


                        const counter =
                            entry.target;


                        const target =
                            Number(
                                counter.dataset.target
                            );


                        let count = 0;


                        function updateCounter() {


                            const increment =
                                Math.ceil(
                                    target / 60
                                );


                            count += increment;


                            if (
                                count >= target
                            ) {

                                counter.textContent =
                                    target;

                            } else {

                                counter.textContent =
                                    count;


                                requestAnimationFrame(
                                    updateCounter
                                );

                            }

                        }


                        updateCounter();


                        counterObserver.unobserve(
                            counter
                        );


                    }
                );


            }
        );


    counters.forEach(
        function (counter) {

            counterObserver.observe(
                counter
            );

        }
    );

}



/* =====================================================
   BACK TO TOP BUTTON
===================================================== */

const backToTop =
    document.getElementById(
        "backToTop"
    );


if (backToTop) {


    window.addEventListener(
        "scroll",
        function () {


            if (
                window.scrollY > 500
            ) {

                backToTop.classList.add(
                    "show"
                );

            } else {

                backToTop.classList.remove(
                    "show"
                );

            }

        }
    );


    backToTop.addEventListener(
        "click",
        function () {


            window.scrollTo({

                top: 0,

                behavior: "smooth"

            });


        }
    );

}



/* =====================================================
   ACTIVE NAVIGATION
   MULTI-PAGE WEBSITE
===================================================== */

document.addEventListener(
    "DOMContentLoaded",
    function () {


        const navItems =
            document.querySelectorAll(
                ".nav-links a"
            );


        if (navItems.length === 0) {

            return;

        }


        /* Get current page */

        let currentPage =
            window.location.pathname
                .split("/")
                .pop();


        /* Remove query/hash */

        currentPage =
            currentPage.split("?")[0];

        currentPage =
            currentPage.split("#")[0];


        /* Home */

        if (
            currentPage === "" ||
            currentPage === "/"
        ) {

            currentPage =
                "index.html";

        }


        navItems.forEach(
            function (link) {


                link.classList.remove(
                    "active"
                );


                const href =
                    link.getAttribute(
                        "href"
                    );


                if (!href) {

                    return;

                }


                /* Clean href */

                const cleanHref =
                    href
                        .replace("/", "")
                        .replace(".html", "");


                let pageName =
                    currentPage
                        .replace(".html", "");


                /* Home */

                if (
                    pageName === ""
                ) {

                    pageName =
                        "index";

                }


                if (
                    cleanHref === pageName
                ) {

                    link.classList.add(
                        "active"
                    );

                }

            }
        );


    }
);


/* =====================================================
   CONTACT FORM
===================================================== */

const contactForm = document.getElementById("contactForm");

if (contactForm) {

    contactForm.addEventListener("submit", async function (event) {

        event.preventDefault();

        const formMessage =
            document.getElementById("form-message");

        const sendButton =
            document.getElementById("sendButton");

        const name =
            document.getElementById("name").value.trim();

        const email =
            document.getElementById("email").value.trim();

        const subject =
            document.getElementById("subject").value.trim();

        const message =
            document.getElementById("message").value.trim();


        if (!name || !email || !subject || !message) {

            formMessage.textContent =
                "Please fill in all fields.";

            formMessage.style.color =
                "#ff6b6b";

            return;
        }


        sendButton.disabled = true;

        sendButton.innerHTML =
            'Sending... <i class="fas fa-spinner fa-spin"></i>';

        formMessage.textContent =
            "Sending your message...";

        formMessage.style.color =
            "#ffffff";


        try {

            const response = await fetch(
                "/api/contact",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        name: name,
                        email: email,
                        subject: subject,
                        message: message
                    })
                }
            );


            const result = await response.json();


            if (response.ok && result.success) {

                formMessage.textContent =
                    "Message sent successfully! Thank you.";

                formMessage.style.color =
                    "#4ade80";

                contactForm.reset();

            } else {

                formMessage.textContent =
                    result.message ||
                    "Unable to send your message.";

                formMessage.style.color =
                    "#ff6b6b";
            }


        } catch (error) {

            console.error(
                "Contact form error:",
                error
            );

            formMessage.textContent =
                "Something went wrong. Please try again.";

            formMessage.style.color =
                "#ff6b6b";
        }


        sendButton.disabled = false;

        sendButton.innerHTML =
            'Send Message <i class="fas fa-paper-plane"></i>';

    });

}


/* =====================================================
   PROJECT CARD TILT EFFECT
===================================================== */

const projectCards =
    document.querySelectorAll(
        ".project-card"
    );


projectCards.forEach(
    function (card) {


        card.addEventListener(
            "mousemove",
            function (event) {


                const rect =
                    card.getBoundingClientRect();


                const x =
                    event.clientX -
                    rect.left;


                const y =
                    event.clientY -
                    rect.top;


                const centerX =
                    rect.width / 2;


                const centerY =
                    rect.height / 2;


                const rotateX =
                    (y - centerY) / 20;


                const rotateY =
                    (centerX - x) / 20;


                card.style.transform =
                    `perspective(800px)
                     rotateX(${rotateX}deg)
                     rotateY(${rotateY}deg)
                     translateY(-5px)`;


            }
        );



        card.addEventListener(
            "mouseleave",
            function () {


                card.style.transform =
                    "perspective(800px) " +
                    "rotateX(0deg) " +
                    "rotateY(0deg)";


            }
        );


    }
);



/* =====================================================
   PAGE LOADED
===================================================== */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        document.body.classList.add(
            "page-loaded"
        );

    }
);