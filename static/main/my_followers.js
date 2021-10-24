const loadMoreUserButton = document.getElementById('load_more_user');
if (loadMoreUserButton) {
  loadMoreUserButton.addEventListener('click', loadMoreUser);
  const followersUsers = document.querySelector('.fwr_users');

  async function loadMoreUser() {
    const lastUser = document.querySelector('.last_follower');
    const { follower_pk } = lastUser.dataset;
    const { url_root } = lastUser.dataset;

    lastUser.classList.remove('last_follower');
    lastUser.removeAttribute('data-follower_pk');
    lastUser.removeAttribute('data-url_root');

    const response = await fetch(`${url_root}?lastUserId=${ follower_pk }`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });
    const json = await response.json();

    const result = json['data'];

    if (!result) {
      loadMoreUserButton.style.display = 'none';
    } else {
      result.forEach((item) => {
        const users = document.createElement('div');
        users.classList.add('text-left');
        users.innerHTML = `<p><img class="rounded-circle ml-1" src="${item.avatar}"
                                width="50" height="40" alt="image"/><a href="/by_user/${item.pk}" style="color: #b3c7e1; text-decoration: none; font-size: 20px">
                                ${item.user}</a></div>`;

        if (item.last_follower) {
          users.classList.add('last_follower');
          users.setAttribute('data-follower_pk', item.pk);
          users.setAttribute('data-url_root', url_root);
        }

        followersUsers.append(users);
      });
    }
  }
}