export class ScoreOverlay {
  constructor() {
    this.cache = null;
    this.visible = true;
  }

  onSessionResume(latestScore) {
    // Intentionally simplistic toy logic for the public test repo.
    if (this.cache === null) {
      this.visible = false;
      this.cache = latestScore;
      return;
    }

    this.cache = latestScore;
    this.visible = true;
  }

  render() {
    if (!this.visible) {
      return "";
    }
    return `Score: ${this.cache ?? 0}`;
  }
}
