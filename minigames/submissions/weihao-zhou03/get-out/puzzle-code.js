/* Board exchange keeps the initial rail phase as well as the floor layout. */
(function(root) {
  'use strict';
  const format = 'get-out-moving-walls-v1';
  function encode(board, movers = []) {
    return movers.length ? JSON.stringify({format, board, movers}, null, 2) : board.join('\n');
  }
  function decode(text) {
    const value = text.trim();
    if (value.startsWith('{')) {
      let puzzle;
      try { puzzle = JSON.parse(value); }
      catch { throw new Error('The moving-wall code is incomplete. Copy the whole code and try again.'); }
      if (puzzle.format !== format || !Array.isArray(puzzle.board) || !Array.isArray(puzzle.movers)) {
        throw new Error('Use a Moving Walls board code, or a plain S / E / # / . board.');
      }
      return {board: puzzle.board, movers: puzzle.movers};
    }
    return {board: value.split(/\r?\n/).map(row => row.trim()), movers: []};
  }
  const api = {encode, decode};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.GetOutCode = api;
})(globalThis);
