const API_BASE_URL = "http://localhost:5000/"

async function fetchPriority(data = {}) {
    try {
        showLoading();
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
async function fetchItems() {
    try {
        const response = await fetch(API_BASE_URL + "items", {
            "method": "GET",
            "headers": {
                "Content-Type": "application/json"
            }
        });
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const result = await response.json();
        console.log('Response from server:', result);
        return result;      
    } catch (error) {
        console.error('Error during GET request:', error);
        return null;
    }
}
async function addItem() {
    const itemInput = document.getElementById("new_item");
    const item = itemInput.value.trim();
    if (item === "") {
        return;
    }
    const data = {
        "item": item
    };

    try {
        const response = await fetch(API_BASE_URL + "add_item", {
            "method": "POST",
            "headers": {
                "Content-Type": "application/json"
            },
            "body": JSON.stringify(data)
        });
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const result = await response.json();
        console.log('Response from server:', result);
        itemInput.value = ""; // Clear the input field
        showPriority();
    } catch (error) {
        console.error('Error during POST request:', error);
    }
}

function hideAll() {
    const element_ids = ["prioritize_container", "new_item_container", "view_list_container", "response_container", "loading_container"];
    element_ids.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.classList.add("hidden");
        }
    });
}
function showLoading() {
    hideAll();
    const container = document.getElementById("loading_container");
    if (container) {
        container.classList.remove("hidden");
    }
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
async function showViewList() {
    hideAll();
    const container = document.getElementById("view_list_container");
    if (container) {
        container.classList.remove("hidden");
    }
    document.getElementById("loading").classList.remove("hidden");
    document.getElementById("todo_list").classList.add("hidden");

    items_data = await fetchItems();
    // remove previous list items
    const todoList = document.getElementById("todo_list");
    while (todoList.firstChild) {
        todoList.removeChild(todoList.firstChild);
    }
    items_data["items"].forEach(element => {
        const li = document.createElement("li");
        li.textContent = element;
        todoList.appendChild(li);
    });
    document.getElementById("loading").classList.add("hidden");
    document.getElementById("todo_list").classList.remove("hidden");
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