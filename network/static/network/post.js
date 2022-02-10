const editeBtn = document.querySelector("#edite-btn");
let errorEditeField;
let postId;
let contentFormEl;
let contentEl;

const submit_edited_form = function (e) {
  e.preventDefault();
  const csrftoken = getCookie("csrftoken");
  
  fetch("/edite-form/" + parseInt(postId), {
    method: "POST",
    body: JSON.stringify({
      content: contentFormEl.elements["content"].value,
    }),
    headers: { "X-CSRFToken": csrftoken },
  })
    .then((response) => response.json())
    .then((result) => {
      console.log(result.error)
      if (result.error) errorEditeField.textContent = result.error;
      else {
        contentEl.textContent = result.content;
        contentEl.style.display = "block";
        contentFormEl.style.display = "none";
        editeBtn.style.block = "block";
      }
    });
};

const editePost = function (e) {
  e.preventDefault();
  postId = e.target.dataset.postId;
  contentEl = e.target.closest("#post").querySelector("#content");
  contentFormEl = e.target.closest("#post").querySelector("#contentForm");
  errorEditeField = e.target.closest("#post").querySelector("#error");
  
  // display contentform and hide content
  editeBtn.style.block = "none";
  contentEl.style.display = "none";
  contentFormEl.style.display = "block";

  contentFormEl.addEventListener("submit", submit_edited_form.bind(this));
};

editeBtn?.addEventListener("click", editePost);
