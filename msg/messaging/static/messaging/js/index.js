
const searchIcon = document.getElementById('search-input');
searchIcon.addEventListener('click', () => {
    if (isCollapsed) {
        isCollapsed = false;
        sidebar.classList.remove('collapsed');
        adjustSidebarTop();
    }
});
// Toggle sidebar collapse

let isCollapsed = window.innerWidth < 550;

document.getElementById('toggleBtn').addEventListener('click', () => {

    isCollapsed = !isCollapsed;
    // console.log(isCollapsed)
    sidebar.classList.toggle('collapsed', isCollapsed);
});

document.getElementById('search-input').addEventListener('input', function () {
    const searchValue = this.value.toLowerCase();
    const userList = document.getElementById('userList');
    const users = userList.getElementsByTagName('li');

    for (let user of users) {
        const username = user.querySelector('.item-name').textContent.toLowerCase();
        if (username.includes(searchValue)) {
            user.style.display = ''; // Show the user
        } else {
            user.style.display = 'none'; // Hide the user
        }
    }
});

let activeItem = null;

function setActive(item) {
    // Remove active class from the currently active item, if any
    if (activeItem) {
        activeItem.classList.remove('active');
    }

    // Add active class to the clicked item
    item.classList.add('active');

    // Set the active item to the currently clicked item
    activeItem = item;
}



document.addEventListener("DOMContentLoaded", () => {
    adjustMessageWidth();
    adjustSidebarTop();
    checkSidebarWidth();
    collapseSidebarOnSmallScreen();
});

const resizeEvents = debounce(() => {
    adjustMessageWidth();
    adjustSidebarTop();
    checkSidebarWidth();
    collapseSidebarOnSmallScreen();
}, 100);

// Ensure resizeEvents is defined
window.addEventListener('resize', resizeEvents);



// Adjust sidebar top when toggle button is clicked
document.getElementById('toggleBtn1').addEventListener('click', () => {
    adjustSidebarTop();
    const intervalId = setInterval(adjustSidebarTop, 10);
    setTimeout(() => clearInterval(intervalId), 1000);
});

// Add click event listener to each element with the class 'navlink'
Array.from(document.getElementsByClassName('navlink')).forEach(element => {
    element.addEventListener('click', () => {
        adjustSidebarTop();
        const intervalId = setInterval(adjustSidebarTop, 10);
        setTimeout(() => clearInterval(intervalId), 1000);
    });
});


const sidebar = document.getElementById('sidebar');
const sidebarObserver = new ResizeObserver(() => adjustMessageWidth());
if (sidebar) {
    sidebarObserver.observe(sidebar);
}

const resizeObserver = new ResizeObserver(checkSidebarWidth);
resizeObserver.observe(sidebar);

const sidebarResizer = document.createElement('div');
sidebarResizer.className = 'sidebar-resizer';
sidebar.appendChild(sidebarResizer);

sidebarResizer.addEventListener('mousedown', (e) => {
    e.preventDefault();
    document.addEventListener('mousemove', resizeSidebar);
    document.addEventListener('mouseup', stopResizing);
});

function adjustMessageWidth() {
    const sidebarWidth = sidebar.offsetWidth;
    const messages = document.querySelector('.message-container');
    messages.style.width = `${sidebarWidth}px`;
}

function adjustSidebarTop() {
    const navbarHeight = document.querySelector('.navbar').offsetHeight;
    sidebar.style.top = `${navbarHeight}px`;
    sidebar.style.height = `calc(100% - ${navbarHeight}px)`;
}

function checkSidebarWidth() {
    if (sidebar.offsetWidth < 120) {
        sidebar.classList.add('icon-only');
    } else {
        sidebar.classList.remove('icon-only');
    }
}

function collapseSidebarOnSmallScreen() {
    if (window.innerWidth < 550) {
        sidebar.classList.add('collapsed');
        isCollapsed = 'true'
    }
    checkSidebarWidth();
}

function resizeSidebar(e) {
    const newWidth = e.clientX;
    sidebar.style.width = `${Math.min(500, Math.max(80, newWidth))}px`;
}

function stopResizing() {
    document.removeEventListener('mousemove', resizeSidebar);
    document.removeEventListener('mouseup', stopResizing);
}
let receiver_msg = ""
function fetchMessages(userId) {
    const url = `/messaging/messages/${userId}/`;
    receiver_msg = `${userId}`
    fetch(url)
        .then(response => response.json())
        .then(data => {
            length_of_messages = data.length
            console.log(length_of_messages)
            const messageContainer = document.getElementById('messageContainer');
            messageContainer.innerHTML = '';
            data.forEach(message => {
                const messageElement = document.createElement('div');
                messageElement.className = message.sender__username === userId ? 'sender' : 'receiver';
                messageElement.classList.add('message');
                messageElement.innerHTML = `
                        <div class='message-part'>
    <div class='message-content'>${message.content}</div>
    ${message.media_image ? `
    <div class='message-image'>
    <img src="${message.media_image}" alt="Message Image" onclick="openModal('${message.media_image}','${message.content}')">
</div>` : ''}</div>
    <div class='message-timestamp'>${new Date(message.timestamp).toLocaleString()}</div>
</div>
                    `;
                messageContainer.appendChild(messageElement);
                const container = document.getElementById('messageContainer');
                container.scrollTop = container.scrollHeight;

            });

        })
        .catch(error => console.error('Error fetching messages:', error));
}


// Debounce function to limit the rate at which a function can fire
function debounce(func, wait) {
    let timeout;
    return function (...args) {
        const context = this;
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(context, args), wait);
    };
}
function toggleDropdown() {
    var dropdownMenu = document.getElementById('dropdownMenu');
    dropdownMenu.classList.toggle('show');
}

// Close dropdown when clicking outside
window.onclick = function (event) {
    if (!event.target.matches('.dropdown-toggle')) {
        var dropdowns = document.getElementsByClassName("dropdown-menu");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
};

document.getElementById('messageForm').addEventListener('submit', function (e) {
    e.preventDefault();
    // Handle message sending logic here
});

// Function to open the modal
function openModal(src, caption) {
    document.getElementById('myModal').style.display = 'flex';
    document.getElementById('modalImage').src = src;
    document.getElementById('caption').innerText = caption
    document.getElementById('downloadLink').href = src;
}

// Function to close the modal
function closeModal() {
    document.getElementById('myModal').style.display = 'none';
}

// Close the modal when clicking outside the image
window.onclick = function (event) {
    if (event.target == document.getElementById('myModal')) {
        closeModal();
    }
}

document.getElementById('caption').addEventListener('scroll', function () {
    const el = this;
    const scrollTop = el.scrollTop;
    const maxScroll = el.scrollHeight - el.clientHeight;

    if (scrollTop === 0) {
        el.classList.remove('scrolling');
    } else if (scrollTop >= maxScroll) {
        el.classList.remove('scrolling');
    } else {
        el.classList.add('scrolling');
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const openPopupButton = document.getElementById('openChatPopup');
    const closePopupButton = document.getElementById('closePopup');
    const chatPopup = document.getElementById('chatPopup');
    const searchInput = document.getElementById('searchInput');
    const userListPopup = document.getElementById('userListPopup');
    const new_chat = document.getElementById('new_chat')
    // Function to open the popup
    openPopupButton.addEventListener('click', function () {
        console.log('open')
        isCollapsed=false
        sidebar.classList.toggle('collapsed', isCollapsed);
        
        new_chat.innerHTML = ""
        chatPopup.classList.add('show');
        fetchUserList();
    });

    // Function to close the popup
    closePopupButton.addEventListener('click', close_button)
    function close_button() {
        new_chat.innerHTML = '<button id="openChatPopup" class="newchatbutton"><i class="fas fa-comment-dots"></i> New</button>'
        button_update()
        document.getElementById('openChatPopup').addEventListener('click', function () {
            console.log('open')
        isCollapsed=false
        sidebar.classList.toggle('collapsed', isCollapsed);
            new_chat.innerHTML = chatPopup.outerHTML
            chatPopup.classList.add('show');
            fetchUserList();
        });
        chatPopup.classList.remove('show');
    }

    // Function to filter users based on search input
    function checkCollapseStatus() {
        if (isCollapsed==true   ) {
            close_button();
        }
    }
    
    // Periodically check if isCollapsed has changed
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.attributeName === 'class') {
                // Update isCollapsed based on whether the sidebar has the 'collapsed' class
                isCollapsed = sidebar.classList.contains('collapsed');
                // Call checkCollapseStatus() when class changes
                checkCollapseStatus();
            }
        });
    });
    
    // Configure the observer to watch for attribute changes
    observer.observe(sidebar, {
        attributes: true // Watch for attribute changes
    });

    // Fetch user list and populate the popup
    function fetchUserList(query = '') {
        fetch(`/messaging/users/?search=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(users => {
                userListPopup.innerHTML = ''; // Clear existing users
                users.forEach(user => {
                    const li = document.createElement('li');
                    li.textContent = user.username;
                    li.addEventListener('click', () => {
                        fetchMessages(user.username);
                        receiver_msg = user.username;
                        chatPopup.style.display = 'none';
                        item = document.getElementById(`user-${user.username}`);
                        close_button()
                        collapseSidebarOnSmallScreen()

                        if (activeItem) {
                            activeItem.classList.remove('active');
                        }
                        item.classList.add('active');
                        activeItem = item;

                    });

                    userListPopup.appendChild(li);
                });
            });
    }

    searchInput.addEventListener('input', function () {
        const filter = searchInput.value.toLowerCase();
        fetchUserList(filter); // Fetch and filter user list based on input
    });

    function selectUser(username) {
        console.log(`Selected user: ${username}`);
        // Add logic to handle the selected user
        chatPopup.style.display = 'none'; // Close the popup after selection
    }
});


window.addEventListener('load', updateUserList)
async function updateUserList() {
    try {
        const response = await fetch('/messaging/messages_list/users'); // Replace with your API endpoint
        const users = await response.json();
        const userList = document.getElementById('userList');
        userList.innerHTML = ''; // Clear existing user list

        users.forEach(user => {
            const li = document.createElement('li');
            li.id = `user-${user.username}`;
            li.onclick = () => {

                setActive(li);
                collapseSidebarOnSmallScreen();
                fetchMessages(user.username);
                
            };

            const img = document.createElement('img');
            img.className = 'icon';
            img.alt = user.username;
            img.src = user.profile__profile_photo ? `/messaging/media/${user.profile__profile_photo}` : '/static/messaging/images/icon/default-user-image.png';

            const span = document.createElement('span');
            span.className = 'item-name';
            span.textContent = user.username;

            li.appendChild(img);
            li.appendChild(span);
            userList.appendChild(li);
        });

        // Ensure the following code runs after the list is updated
        const item = document.getElementById(`user-${receiver_msg}`);
        if (activeItem) {
            activeItem.classList.remove('active');
        }
        if (item) {
            item.classList.add('active');
            activeItem = item;
        } else {
            console.log('Element not found');
        }
    } catch (error) {
        console.error('Error updating user list:', error);
    }
}


document.addEventListener('DOMContentLoaded', button_update());
function button_update() {
    const button = document.getElementById('openChatPopup');
    const chat = document.getElementById('new_chat')
    function updateButtonText() {
        if (chat.offsetWidth < 120) {
            button.innerHTML = '<i class="fas fa-comment-dots"></i>'; // Clear content if width is less than 100px
        } else {
            button.innerHTML = '<i class="fas fa-comment-dots"></i> New'; // Set content when width is 100px or more
        }
    }

    // Initial check
    updateButtonText();

    // Create a ResizeObserver to monitor changes to the button's size
    const resizeObserver = new ResizeObserver(() => {
        updateButtonText();
    });

    // Observe the button for size changes
    resizeObserver.observe(chat);
}
