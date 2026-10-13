/* Get Out! classroom adaptation. Pure rules shared by browser and Node. */
(function (root) {
  'use strict';
  const directions = {up: [-1, 0], right: [0, 1], down: [1, 0], left: [0, -1]};
  function create(board) {
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
    return {board: board.slice(), position: [r, board[r].indexOf('S')], moves: 0, won: false, portals: [null, null]};
  }
  function portalTarget(state, position) {
    const [r,c]=position,[pr,pc]=state.position;
    if(!Number.isInteger(r)||!Number.isInteger(c)||state.board[r]?.[c]!=='#') throw new Error('Choose a wall.');
    if(r!==pr&&c!==pc) throw new Error('Shoot in a straight row or column from your position.');
    const dr=Math.sign(r-pr),dc=Math.sign(c-pc);
    let nr=pr+dr,nc=pc+dc;
    while(nr!==r||nc!==c){
      if(state.board[nr][nc]==='#')throw new Error('Another wall blocks that shot.');
      nr+=dr;nc+=dc;
    }
    const direction=dr>0?'up':dr<0?'down':dc>0?'left':'right';
    return {position:position.slice(),direction};
  }
  function placePortal(state, slot, position) {
    if(state.won)throw new Error('Reset before placing portals.');
    if(![0,1].includes(slot))throw new Error('Choose blue or orange.');
    const target=portalTarget(state,position);
    if(state.portals[1-slot]?.position.join(',')===position.join(','))throw new Error('Choose two different walls.');
    const portals=state.portals.slice();portals[slot]=target;
    return {...state,portals,route:[]};
  }
  function step(state, action) {
    if (!Object.hasOwn(directions, action)) throw new Error('Unknown direction.');
    if (state.won) return state;
    let [dr, dc] = directions[action], [r,c]=state.position;
    const route=[],seen=new Set();
    while(true){
      const key=[r,c,dr,dc].join(',');
      if(seen.has(key)) return state;
      seen.add(key);
      const nr=r+dr,nc=c+dc;
      if(nr<0||nr>=state.board.length||nc<0||nc>=state.board[0].length)break;
      if(state.board[nr][nc]==='#'){
        const slot=state.portals.findIndex(p=>p&&p.position[0]===nr&&p.position[1]===nc);
        if(slot<0||!state.portals[1-slot])break;
        const face=directions[state.portals[slot].direction];
        if(dr!==-face[0]||dc!==-face[1])break;
        const out=state.portals[1-slot];
        const er=out.position[0]+dr,ec=out.position[1]+dc;
        if(er<0||er>=state.board.length||ec<0||ec>=state.board[0].length||state.board[er][ec]==='#')break;
        r=er;c=ec;route.push({position:[r,c],jump:true});
      }else{r=nr;c=nc;route.push({position:[r,c],jump:false});}
      if(state.board[r][c]==='E')break;
    }
    if(r===state.position[0]&&c===state.position[1])return state;
    return {...state,position:[r,c],moves:state.moves+1,won:state.board[r][c]==='E',route};
  }
  function legalActions(state) {
    return Object.keys(directions).filter(action => step(state, action) !== state);
  }
  function observe(state) {
    return {board: state.board.slice(), position: state.position.slice(), moves: state.moves,
      portals: state.portals.map(p=>p?{position:p.position.slice(),direction:p.direction}:null), won: state.won, legalActions: legalActions(state)};
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
  const api = {create, portalTarget, placePortal, step, legalActions, observe, solve};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.GetOut = api;
})(globalThis);
