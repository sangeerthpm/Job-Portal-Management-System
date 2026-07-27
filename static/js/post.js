function toggleComments(postId, btn) {
    const commentsDiv = document.getElementById("comments-" + postId);
    if (!commentsDiv) {
        console.error("No comments div found for post", postId);
        return;
    }

    if (commentsDiv.classList.contains("hidden")) {
        commentsDiv.classList.remove("hidden");
        btn.innerText = "Hide comments";
    } else {
        commentsDiv.classList.add("hidden");
        btn.innerText = "View all comments";
    }
}