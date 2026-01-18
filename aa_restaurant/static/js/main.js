function safeParseJson(value, fallback) {
    if (!value) {
        return fallback;
    }
    try {
        var parsed = JSON.parse(value);
        return parsed == null ? fallback : parsed;
    } catch (e) {
        return fallback;
    }
}

function getCart() {
    var raw = localStorage.getItem("aaCart");
    var cart = safeParseJson(raw, []);
    if (!Array.isArray(cart)) {
        return [];
    }
    return cart;
}

function saveCart(cart) {
    localStorage.setItem("aaCart", JSON.stringify(cart || []));
}

function getOrders() {
    var raw = localStorage.getItem("aaOrders");
    var orders = safeParseJson(raw, []);
    if (!Array.isArray(orders)) {
        return [];
    }
    return orders;
}

function saveOrders(orders) {
    localStorage.setItem("aaOrders", JSON.stringify(orders || []));
}

function updateCartBadge() {
    var badge = document.getElementById("cartCountBadge");
    if (!badge) {
        return;
    }
    var url = badge.getAttribute("data-cart-count-url");
    if (!url) {
        var cart = getCart();
        var count = 0;
        for (var i = 0; i < cart.length; i++) {
            var qty = cart[i].quantity || 0;
            count += qty;
        }
        if (count <= 0) {
            badge.textContent = "0";
            badge.classList.add("d-none");
        } else {
            badge.textContent = String(count);
            badge.classList.remove("d-none");
        }
        return;
    }

    fetch(url, { credentials: "same-origin" })
        .then(function (response) {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then(function (data) {
            var count = data && typeof data.cart_count === "number" ? data.cart_count : 0;
            if (count <= 0) {
                badge.textContent = "0";
                badge.classList.add("d-none");
            } else {
                badge.textContent = String(count);
                badge.classList.remove("d-none");
            }
        })
        .catch(function () {
            var cart = getCart();
            var count = 0;
            for (var i = 0; i < cart.length; i++) {
                var qty = cart[i].quantity || 0;
                count += qty;
            }
            if (count <= 0) {
                badge.textContent = "0";
                badge.classList.add("d-none");
            } else {
                badge.textContent = String(count);
                badge.classList.remove("d-none");
            }
        });
}

function getCurrentUser() {
    var raw = localStorage.getItem("aaCurrentUser");
    return safeParseJson(raw, null);
}

function setLoggedInUser(user) {
    localStorage.setItem("aaLoggedIn", "true");
    localStorage.setItem("aaCurrentUser", JSON.stringify(user || {}));
}

function clearLoginState() {
    localStorage.removeItem("aaLoggedIn");
    localStorage.removeItem("aaCurrentUser");
}

function showLoginModal() {
    var modalElement = document.getElementById("loginModal");
    if (!modalElement || typeof bootstrap === "undefined" || !bootstrap.Modal) {
        return;
    }
    var modal = bootstrap.Modal.getOrCreateInstance(modalElement);
    modal.show();
}

function updateNavbarAuth() {
    var loggedIn = localStorage.getItem("aaLoggedIn") === "true";
    var user = loggedIn ? getCurrentUser() : null;

    var loggedOutContainer = document.getElementById("navAuthLoggedOut");
    var loggedInContainer = document.getElementById("navAuthLoggedIn");
    var nameSpan = document.getElementById("navUserName");

    if (!loggedOutContainer || !loggedInContainer) {
        return;
    }

    if (loggedIn && user && user.name) {
        loggedOutContainer.classList.add("d-none");
        loggedInContainer.classList.remove("d-none");
        if (nameSpan) {
            nameSpan.textContent = user.name;
        }
    } else {
        loggedOutContainer.classList.remove("d-none");
        loggedInContainer.classList.add("d-none");
        if (nameSpan) {
            nameSpan.textContent = "";
        }
    }
}

function handleLoginSubmit() {
    var emailInput = document.getElementById("loginEmail");
    var passwordInput = document.getElementById("loginPassword");
    if (!emailInput || !passwordInput) {
        return;
    }

    var email = emailInput.value || "";
    var name = email.split("@")[0] || "Guest";

    setLoggedInUser({
        name: name,
        email: email
    });

    updateNavbarAuth();

    var modalElement = document.getElementById("loginModal");
    if (modalElement && typeof bootstrap !== "undefined" && bootstrap.Modal) {
        var modal = bootstrap.Modal.getInstance(modalElement) || bootstrap.Modal.getOrCreateInstance(modalElement);
        modal.hide();
    }
}

function handleSignupSubmit() {
    var nameInput = document.getElementById("signupName");
    var emailInput = document.getElementById("signupEmail");
    var passwordInput = document.getElementById("signupPassword");
    if (!nameInput || !emailInput || !passwordInput) {
        return;
    }

    var name = nameInput.value || "Guest";
    var email = emailInput.value || "";

    setLoggedInUser({
        name: name,
        email: email
    });

    updateNavbarAuth();

    var modalElement = document.getElementById("signupModal");
    if (modalElement && typeof bootstrap !== "undefined" && bootstrap.Modal) {
        var modal = bootstrap.Modal.getInstance(modalElement) || bootstrap.Modal.getOrCreateInstance(modalElement);
        modal.hide();
    }
}

function handleLogout() {
    clearLoginState();
    updateNavbarAuth();
}

document.addEventListener("DOMContentLoaded", function () {
    updateNavbarAuth();
    updateCartBadge();

    var loginButton = document.getElementById("loginSubmitButton");
    if (loginButton) {
        loginButton.addEventListener("click", function (event) {
            event.preventDefault();
            handleLoginSubmit();
        });
    }

    var signupButton = document.getElementById("signupSubmitButton");
    if (signupButton) {
        signupButton.addEventListener("click", function (event) {
            event.preventDefault();
            handleSignupSubmit();
        });
    }

    var logoutButton = document.getElementById("logoutButton");
    if (logoutButton) {
        logoutButton.addEventListener("click", function (event) {
            event.preventDefault();
            handleLogout();
        });
    }
});

window.getCart = getCart;
window.saveCart = saveCart;
window.updateCartBadge = updateCartBadge;
window.getOrders = getOrders;
window.saveOrders = saveOrders;
window.showLoginModal = showLoginModal;
