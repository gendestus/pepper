const API_BASE_URL = "http://localhost:5000/"

async function fetchPriority(data = {}) {
    try {
        const response = await fetch(API_BASE_URL + "priority", {
            "method": "POST",
            "headers": {
                "Content-Type": "application/json"
            },
            "body": JSON.stringify(data)
        });
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const result = await response.text();
        console.log('Response from server:', result);
        showResponse(result);
        return result;      
    } catch (error) {
        console.error('Error during POST request:', error);
        return null;
    }
}

function hideAll() {
    const element_ids = ["prioritize_container", "new_item_container", "view_list_container", "response_container"];
    element_ids.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.classList.add("hidden");
        }
    });
}

function showPriority() {
    hideAll();
    const container = document.getElementById("prioritize_container");
    if (container) {
        container.classList.remove("hidden");
    }
}

function showNewItem() {
    hideAll();
    const container = document.getElementById("new_item_container");
    if (container) {
        container.classList.remove("hidden");
    }
}
function showViewList() {
    hideAll();
    const container = document.getElementById("view_list_container");
    if (container) {
        container.classList.remove("hidden");
    }
}
function showResponse(response) {
    hideAll();
    const container = document.getElementById("response_container");
    if (container) {
        container.classList.remove("hidden");
        const responseText = document.getElementById("response_text");
        if (responseText) {
            responseText.textContent = response;
        }
    }
}