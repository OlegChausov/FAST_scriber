
 document.addEventListener('DOMContentLoaded', function () {
    const allAudio = document.querySelectorAll('audio');

    allAudio.forEach(audio => {
      audio.addEventListener('play', () => {
        allAudio.forEach(other => {
          if (other !== audio && !other.paused) {
            other.pause();
          }
        });
      });
    });
  });


