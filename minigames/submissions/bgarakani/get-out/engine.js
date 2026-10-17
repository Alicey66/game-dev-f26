/* Get Out! classroom adaptation. Pure rules shared by browser and Node. */
(function (root) {
  'use strict';
  const directions = {up: [-1, 0], right: [0, 1], down: [1, 0], left: [0, -1]};
  function create(board) {
    if (!Array.isArray(board) || board.length < 2 || board.length > 42 ||
        typeof board[0] !== 'string' || board[0].length < 2 || board[0].length > 42 ||
        board.some(row => typeof row !== 'string' || row.length !== board[0].length || /[^.#SE]/.test(row))) {
      throw new Error('Use a rectangular board, 2–42 rows and columns, with only S, E, #, and .');
    }
    const all = board.join('');
    if (all.split('S').length !== 2 || all.split('E').length !== 2) {
      throw new Error('Place exactly one start (S) and one exit (E).');
    }
    const r = board.findIndex(row => row.includes('S'));
    const state = {board: board.slice(), position: [r, board[r].indexOf('S')], moves: 0, won: false, failed: false};
    const path = solve(state);
    const minimumMoves = path === null ? null : path.length;
    const size = Math.max(7, board.length, board[0].length);
    // Integer arithmetic avoids rounding drift; extra moves taper from 100% to 0%.
    const moveLimit = minimumMoves === null ? null : minimumMoves + Math.floor(minimumMoves * (42 - size) / 35);
    return {...state, minimumMoves, moveLimit};
  }
  function step(state, action) {
    if (!Object.hasOwn(directions, action)) throw new Error('Unknown direction.');
    if (state.won || state.failed) return state;
    const [dr, dc] = directions[action];
    let [r, c] = state.position;
    while (true) {
      const nr = r + dr, nc = c + dc;
      if (nr < 0 || nr >= state.board.length || nc < 0 || nc >= state.board[0].length || state.board[nr][nc] === '#') break;
      r = nr; c = nc;
      if (state.board[r][c] === 'E') break;
    }
    if (r === state.position[0] && c === state.position[1]) return state;
    const moves = state.moves + 1, won = state.board[r][c] === 'E';
    return {...state, position: [r, c], moves, won,
      failed: !won && state.moveLimit != null && moves >= state.moveLimit};
  }
  function legalActions(state) {
    return Object.keys(directions).filter(action => step(state, action) !== state);
  }
  function observe(state) {
    return {board: state.board.slice(), position: state.position.slice(), moves: state.moves,
      won: state.won, failed: state.failed, minimumMoves: state.minimumMoves, moveLimit: state.moveLimit, legalActions: legalActions(state)};
  }
  function solve(state) {
    const queue = [{state, path: []}], seen = new Set([state.position.join(',')]);
    for (let i = 0; i < queue.length; i++) {
      const item = queue[i];
      if (item.state.won) return item.path;
      for (const action of legalActions(item.state)) {
        const next = step(item.state, action), key = next.position.join(',');
        if (!seen.has(key)) {
          seen.add(key); queue.push({state: next, path: [...item.path, action]});
        }
      }
    }
    return null;
  }
  const api = {create, step, legalActions, observe, solve};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.GetOut = api;
})(globalThis);
