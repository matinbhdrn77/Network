const newPost = document.querySelector("#newPost");
const likeBtn = document.querySelectorAll("#like");
const dislikeBtn = document.querySelectorAll("#dislike")

// Clear post inpyut field
newPost.value = "";

// Find csrfToken (This is not my code)
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const handleLike = function (e) {
  const likeEl = e.target.closest("#like");
  const postId = likeEl.dataset.postId;
  const csrftoken = getCookie("csrftoken");
  fetch(`/like-dislike/${parseInt(postId)}/like`, {
    method: "POST",
    headers: { "X-CSRFToken": csrftoken },
  })
    .then((response) => response.json())
    .then((result) => {
      likeEl.querySelector("a").querySelector("i").textContent =
        result.num_likes;
      likeEl.querySelector("a").className = `u-link-v5 g-color-${result.is_like ? 'primary' : 'gray'}-dark-v4 g-color-primary--hover`

      likeEl.nextElementSibling
        .querySelector("a")
        .querySelector("i").textContent = result.num_dislikes;
        likeEl.nextElementSibling.querySelector("a").className = `u-link-v5 g-color-${result.is_dislike ? 'primary' : 'gray'}-dark-v4 g-color-primary--hover`
    });
};

const handleDislike = function (e) {
  const dislikeEl = e.target.closest("#dislike");
  const postId = dislikeEl.dataset.postId;
  const csrftoken = getCookie("csrftoken");
  fetch(`/like-dislike/${parseInt(postId)}/dislike`, {
    method: "POST",
    headers: { "X-CSRFToken": csrftoken },
  })
    .then((response) => response.json())
    .then((result) => {
      dislikeEl.querySelector("a").querySelector("i").textContent =
        result.num_dislikes;
      dislikeEl.querySelector("a").className = `u-link-v5 g-color-${result.is_dislike ? 'primary' : 'gray'}-dark-v4 g-color-primary--hover`

      dislikeEl.previousElementSibling
        .querySelector("a")
        .querySelector("i").textContent = result.num_likes;
      dislikeEl.previousElementSibling.querySelector("a").className = `u-link-v5 g-color-${result.is_like ? 'primary' : 'gray'}-dark-v4 g-color-primary--hover`
    });
};



likeBtn.forEach((btn) => {
  btn.addEventListener("click", handleLike);
});
dislikeBtn.forEach((btn) => {
  btn.addEventListener("click", handleDislike);
});
