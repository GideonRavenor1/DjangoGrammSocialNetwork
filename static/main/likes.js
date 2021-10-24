function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


document.addEventListener('DOMContentLoaded', onLoad);

function onLoad() {
  const forms = document.querySelectorAll('.like-form');
  Array.from(forms).forEach((form) => {
    form.addEventListener('submit', onSubmit);
  });
}

async function onSubmit(e) {
  e.preventDefault();

  const post_id = e.target.id;

  const data = {post_id};

  try {
    const response = await fetch(`/followers/ajax/count-likes/${post_id}/`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken},
      body: JSON.stringify(data),
    });
    const json = await response.json();

    const result = json['data'];
    const likeButton = document.querySelector(`.like-btn${post_id}`);

    if (result.like) {
      likeButton.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg"
      width="16" height="16" fill="currentColor"
       class="bi bi-heart" viewBox="0 0 16 16">
       <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314
       4.385.92 1.815 2.834 3.989 6.286 6.357
        3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878
       10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824
       1.143c.06.055.119.112.176.171a3.12
       3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"/>
      </svg> ${result.count_likes}`;
    } else {
      likeButton.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
      fill="currentColor" class="bi bi-heart-fill" viewBox="0 0 16 16">
     <path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534
         4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z"/>
     </svg> ${result.count_likes}`;
    }
  } catch (e) {
    console.log('error', e);
  }
}
