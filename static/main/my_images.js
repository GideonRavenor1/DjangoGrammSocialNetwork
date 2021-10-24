const loadMoreUserImageButton = document.getElementById('load_user_image');
if (loadMoreUserImageButton) {
  loadMoreUserImageButton.addEventListener('click', loadMoreUserImage);
  const userImages = document.querySelector('.user_images');

  async function loadMoreUserImage() {
    const lastUserImage = document.querySelector('.last_user_image');
    const { image_pk } = lastUserImage.dataset;
    const { url_root } = lastUserImage.dataset;

    lastUserImage.classList.remove('last_user_image');
    lastUserImage.removeAttribute('data-image_pk');
    lastUserImage.removeAttribute('data-url_root');

    const response = await fetch(`${url_root}?lastUserImageId=${image_pk}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });

    const json = await response.json();

    const result = json['data'];

    if (!result) {
      loadMoreUserImageButton.style.display = 'none';
    } else {
      result.forEach((item) => {
        const images = document.createElement('div');
        images.classList.add('text-left');
        images.innerHTML = `<p><img class="rounded" src="${item.image}" style="width: 40%;" alt="image"/>
            <p><a href="/accounts/profile/delete/${item.pk}/"><svg xmlns="http://www.w3.org/2000/svg"
             width="28" height="28" fill="currentColor" class="bi bi-trash-fill" viewBox="0 0 16 16">
                <path d="M2.5 1a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4h.5a1 1 0 0 0 1-1V2a1
                    1 0 0 0-1-1H10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1H2.5zm3 4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1
                    .5-.5zM8 5a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7A.5.5 0 0 1 8 5zm3 .5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 1 0z"/></svg>
            </a>
            </p>
            </p>
            <p>${item.super_rubric} - ${item.rubric}</p>
            </div>`;

        if (item.last_user_image) {
          images.classList.add('last_user_image');
          images.setAttribute('data-image_pk', item.pk);
          images.setAttribute('data-url_root', url_root);
        }

        userImages.append(images);
      });
    }
  }
}