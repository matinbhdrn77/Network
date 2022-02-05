const newPostForm = document.querySelector("#newPostForm");
const errorField = document.querySelector("#error");
const postsContainer = document.querySelector(".row");
const newPost = document.querySelector("#newPost");

// Clear Fields
errorField.textContent = "";
newPost.value = "";

// Find csrfToken
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

// Submit Form
const submit_form = function (e) {
  e.preventDefault();
  const form = e.target;
  const csrftoken = getCookie("csrftoken");
  fetch("/compose-post", {
    method: "POST",
    body: JSON.stringify({
      content: form.elements["content"].value,
    }),
    headers: { "X-CSRFToken": csrftoken },
  })
    .then((response) => response.json())
    .then((result) => {
      // Check for Errors
      if (result.error) errorField.textContent = result.error;
      else {
        html = `
        <div class="col-md-8">
        <div class="media g-mb-30 media-comment">
          <img
            class="d-flex g-width-50 g-height-50 rounded-circle g-mt-3 g-mr-15"
            src="https://bootdey.com/img/Content/avatar/avatar7.png"
            alt="Profile Image"
          />
          <div class="media-body u-shadow-v18 g-bg-secondary g-pa-30">
            <div class="g-mb-15">
              <h5 class="h5 g-color-gray-dark-v1 mb-0">${result.user}</h5>
              <span class="g-color-gray-dark-v4 g-font-size-12">${result.date}</span>
            </div>
  
            <p>${result.content}</p>
  
            <ul class="list-inline d-sm-flex my-0">
              <li class="list-inline-item g-mr-20">
                <a class="u-link-v5 g-color-gray-dark-v4 g-color-primary--hover" href="#!">
                  <i class="fa fa-thumbs-up g-pos-rel g-top-1 g-mr-3"></i>
                  ${result.like}
                </a>
              </li>
              <li class="list-inline-item g-mr-20">
                <a class="u-link-v5 g-color-gray-dark-v4 g-color-primary--hover" href="#!">
                  <i class="fa fa-thumbs-down g-pos-rel g-top-1 g-mr-3"></i>
                  ${result.dislike}
                </a>
              </li>
              <li class="list-inline-item g-mr-20">
                <a class="u-link-v5 g-color-gray-dark-v4 g-color-primary--hover" href="#!">
                  Edite
                </a>
              </li>
              <li class="list-inline-item ml-auto">
                <a class="u-link-v5 g-color-gray-dark-v4 g-color-primary--hover" href="#!">
                  <i class="fa fa-reply g-pos-rel g-top-1 g-mr-3"></i>
                  Reply
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>
       `;
        postsContainer.insertAdjacentHTML("afterbegin", html);
      }
    });
};

newPostForm.addEventListener("submit", submit_form);
