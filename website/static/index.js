function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function deleteWorkout(workoutId) {
  fetch("/delete-workout", {
    method: "POST",
    body: JSON.stringify({ workoutId: workoutId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}