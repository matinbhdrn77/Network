"use strict";

const followBtn = document.querySelector("#followBtn");
const numFollowers = document.querySelector("#num_followers");

const handleFollowing = function (e) {
  
  fetch(`/handle-following/` + parseInt(e.target.dataset.profileId))
    .then((response) => response.json())
    .then((result) => {
        if (result.action === 'followed') {
            followBtn.textContent = 'Unfollow';
            numFollowers.textContent = result.followers
        }
        else if (result.action === 'unfollowed') {
            followBtn.textContent = 'Follow';
            numFollowers.textContent = result.followers
        }
    });
};

followBtn.addEventListener("click", handleFollowing);
