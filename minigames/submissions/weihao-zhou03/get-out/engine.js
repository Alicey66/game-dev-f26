/* Get Out! classroom adaptation. Pure rules shared by browser and Node. */
(function (root) {
  'use strict';
  const directions = {up: [-1, 0], right: [0, 1], down: [1, 0], left: [0, -1]};
  const same = (a, b) => a[0] === b[0] && a[1] === b[1];
  function create(board, options = {}) {
    if (!Array.isArray(board) || board.length < 2 || board.length > 20 ||
        typeof board[0] !== 'string' || board[0].length < 2 || board[0].length > 20 ||
        board.some(row => typeof row !== 'string' || row.length !== board[0].length || /[^.#SE]/.test(row))) {
      throw new Error('Use a rectangular board, 2–20 rows and columns, with only S, E, #, and .');
    }
    const all = board.join('');
    if (all.split('S').length !== 2 || all.split('E').length !== 2) {
      throw new Error('Place exactly one start (S) and one exit (E).');
    }
    const r = board.findIndex(row => row.includes('S'));
    const position = [r, board[r].indexOf('S')];
    if (!options || typeof options !== 'object') throw new Error('Use valid moving-wall options.');
    const input = options.movers === undefined ? [] : options.movers;
    if (!Array.isArray(input) || input.length > 3) throw new Error('Use at most three moving walls per board.');
    const movers = input.map(mover => {
      if (!mover || !Array.isArray(mover.path) || mover.path.length < 2 || mover.path.length > 20) {
        throw new Error('A rail needs 2–20 adjacent cells in one straight line.');
      }
      const path = mover.path.map(cell => {
        if (!Array.isArray(cell) || cell.length !== 2 || !cell.every(Number.isInteger) ||
            cell[0] < 0 || cell[0] >= board.length || cell[1] < 0 || cell[1] >= board[0].length ||
            !'.S'.includes(board[cell[0]][cell[1]])) {
          throw new Error('Rail cells must be inside the board, on floor or start cells.');
        }
        return cell.slice();
      });
      const delta = [path[1][0] - path[0][0], path[1][1] - path[0][1]];
      if (Math.abs(delta[0]) + Math.abs(delta[1]) !== 1 ||
          path.slice(1).some((cell, i) => cell[0] - path[i][0] !== delta[0] || cell[1] - path[i][1] !== delta[1])) {
        throw new Error('A rail needs adjacent cells in one straight line.');
      }
      const index = mover.index === undefined ? 0 : mover.index;
      const direction = mover.direction === undefined ? 1 : mover.direction;
      if (!Number.isInteger(index) || index < 0 || index >= path.length || ![1,-1].includes(direction)) {
        throw new Error('Choose a valid rail position and direction (1 or -1).');
      }
      if (same(path[index], position)) throw new Error('The moving wall cannot start on the player.');
      return {path, index, direction};
    });
    const railCells = new Set();
    for (const mover of movers) for (const cell of mover.path) {
      const key = cell.join(',');
      if (railCells.has(key)) throw new Error('Moving wall rails cannot cross or overlap.');
      railCells.add(key);
    }
    // Bound the complete search space, including phases created by player holds.
    const searchSize = board.length * board[0].length * movers.reduce((n,m) => n * 2 * m.path.length, 1);
    if (searchSize > 120000) throw new Error('Shorten a rail or use a smaller board for instant route checks and hints.');
    return {board: board.slice(), position, movers, moves: 0, won: false};
  }
  function advanceWall(mover, position) {
    let direction = mover.direction, index = mover.index + direction;
    if (index < 0 || index >= mover.path.length) {
      direction = -direction;
      index = mover.index + direction;
    }
    const held = same(mover.path[index], position);
    return {mover: {...mover, index: held ? mover.index : index, direction}, held,
      targetPosition: mover.path[index]};
  }
  function step(state, action) {
    if (action !== 'wait' && !Object.hasOwn(directions, action)) throw new Error('Unknown direction or action.');
    if (state.won) return state;
    if (action === 'wait' && !state.movers.length) return state;
    let [r, c] = state.position;
    if (action !== 'wait') {
      const [dr, dc] = directions[action];
      while (true) {
        const nr = r + dr, nc = c + dc;
        if (nr < 0 || nr >= state.board.length || nc < 0 || nc >= state.board[0].length ||
            state.board[nr][nc] === '#' || state.movers.some(m => same(m.path[m.index], [nr,nc]))) break;
        r = nr; c = nc;
        if (state.board[r][c] === 'E') break;
      }
      if (r === state.position[0] && c === state.position[1]) return state;
    }
    const position = [r,c], won = state.board[r][c] === 'E';
    const movers = won ? state.movers : state.movers.map(m => advanceWall(m, position).mover);
    return {...state, position, movers, moves: state.moves + 1, won};
  }
  function legalActions(state) {
    if (state.won) return [];
    const actions = Object.keys(directions).filter(action => step(state, action) !== state);
    if (state.movers.length) actions.push('wait');
    return actions;
  }
  function observe(state) {
    return {board: state.board.slice(), position: state.position.slice(), moves: state.moves,
      movers: state.movers.map(m => {
        const next = state.won ? {mover: m, held: false, targetPosition: m.path[m.index]} : advanceWall(m, state.position);
        return {path: m.path.map(cell => cell.slice()), index: m.index, direction: m.direction,
          nextPosition: next.mover.path[next.mover.index].slice(),
          targetPosition: next.targetPosition.slice(), held: next.held};
      }),
      won: state.won, legalActions: legalActions(state)};
  }
  function stateKey(state) {
    return `${state.position.join(',')}|${state.movers.map(m => `${m.index},${m.direction}`).join(';')}`;
  }
  function solve(state) {
    const first = stateKey(state), queue = [state], seen = new Map([[first, null]]);
    for (let i = 0; i < queue.length; i++) {
      const current = queue[i], currentKey = stateKey(current);
      if (current.won) {
        const path = [];
        let key = currentKey;
        while (seen.get(key)) {
          const entry = seen.get(key); path.push(entry.action); key = entry.previous;
        }
        return path.reverse();
      }
      const actions = legalActions(current);
      // Prefer an equally short Wait to an unnecessary out-and-back detour.
      if (actions.includes('wait')) actions.unshift(actions.pop());
      for (const action of actions) {
        const next = step(current, action), key = stateKey(next);
        if (!seen.has(key)) {
          seen.set(key, {previous: currentKey, action}); queue.push(next);
        }
      }
    }
    return null;
  }
  const api = {create, step, legalActions, observe, solve};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.GetOut = api;
})(globalThis);
