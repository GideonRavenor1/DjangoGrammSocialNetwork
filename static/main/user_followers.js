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


document.addEventListener('DOMContentLoaded', onFollowing);

function onFollowing() {
  const form = document.querySelector('.following-form');
  form.addEventListener('submit', onSubmit);
}

async function onSubmit(e) {
  e.preventDefault();

  const user_id = e.target.id;

  const data = { user_id };

  try {
    const response = await fetch(`/followers/ajax/followings/${user_id}/`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken},
      body: JSON.stringify(data),
    });
    const json = await response.json();

    const result = json['data'];
    const followingButton = document.querySelector(`.following-btn${user_id}`);
    const followersCount = document.querySelector(`.followers`);

    if (!result.get_follower) {
      followingButton.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg"
								width="28" height="28" fill="currentColor" class="bi bi-lightbulb-fill" viewBox="0 0 16 16">
								<path d="M2 6a6 6 0 1 1 10.174 4.31c-.203.196-.359.4-.453.619l-.762 1.769A.5.5 0 0 1 10.5 13h-5a.5.5
									0 0 1-.46-.302l-.761-1.77a1.964 1.964 0 0 0-.453-.618A5.984 5.984 0 0 1 2 6zm3 8.5a.5.5 0 0 1 .5-.5h5a.5.5
									0 0 1 0 1l-.224.447a1 1 0 0 1-.894.553H6.618a1 1 0 0 1-.894-.553L5.5 15a.5.5 0 0 1-.5-.5z"/>
										</svg> Подписаться`;
    } else {
      followingButton.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="currentColor"
								class="bi bi-lightbulb" viewBox="0 0 16 16">
								<path d="M2 6a6 6 0 1 1 10.174 4.31c-.203.196-.359.4-.453.619l-.762
								1.769A.5.5 0 0 1 10.5 13a.5.5 0 0 1 0 1 .5.5 0 0 1 0 1l-.224.447a1 1
								0 0 1-.894.553H6.618a1 1 0 0 1-.894-.553L5.5 15a.5.5 0 0 1 0-1 .5.5 0
								0 1 0-1 .5.5 0 0 1-.46-.302l-.761-1.77a1.964 1.964 0 0 0-.453-.618A5.984
								5.984 0 0 1 2 6zm6-5a5 5 0 0 0-3.479 8.592c.263.254.514.564.676.941L5.83
								12h4.342l.632-1.467c.162-.377.413-.687.676-.941A5 5 0 0 0 8 1z"/>
								</svg> Вы подписаны`;
    } if (result.count_followers === 0) {
          followersCount.innerHTML = `<p class="mt-4">Подписчиков нет: <svg xmlns="http://www.w3.org/2000/svg"
                width="28" height="28" fill="currentColor" class="bi bi-person-dash" viewBox="0 0 16 16">
                <path d="M6 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0zm4 8c0 1-1 1-1
                        1H1s-1 0-1-1 1-4 6-4 6 3 6 4zm-1-.004c-.001-.246-.154-.986-.832-1.664C9.516 10.68 8.289 10
                            6 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10z"/>
                <path fill-rule="evenodd" d="M11 7.5a.5.5 0 0 1 .5-.5h4a.5.5 0 0 1 0 1h-4a.5.5 0 0 1-.5-.5z"/>
                                        </svg></p></div>`;
      } else {
        followersCount.innerHTML = `<p>Количество подписчиков: <a href="/followers/list/${result.user_pk}/">
            <button type="submit" class="btn btn-success" name="like">
                        <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="currentColor"
                         class="bi bi-person-check-fill" viewBox="0 0 16 16">
                        <path fill-rule="evenodd" d="M15.854 5.146a.5.5 0 0 1 0 .708l-3 3a.5.5 0 0
                        1-.708 0l-1.5-1.5a.5.5 0 0 1 .708-.708L12.5 7.793l2.646-2.647a.5.5 0 0 1 .708 0z"/>
                        <path d="M1 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1H1zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/>
                        </svg> ${result.count_followers}
                    </button></a></p></div>`;
      }
  } catch (e) {
    console.log('error', e);
  }
}
