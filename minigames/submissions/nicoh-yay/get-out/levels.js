(function(root){
 const levels = [
  {
    "name": "Switchback Vault",
    "prompt": "Find stopping points and new angles for your portal shots.",
    "board": [
      "S.#......#..",
      "#....#.....#",
      ".####..##.#.",
      "#.#.E#....#.",
      ".#......#...",
      ".#..#.......",
      "..#.......##",
      ".#........#.",
      "##...#.....#",
      "#.#.#....#.#",
      ".#..#.....#.",
      "......#.##.."
    ]
  },
  {
    "name": "Crosscurrent",
    "prompt": "Find stopping points and new angles for your portal shots.",
    "board": [
      "S.###..##...#.",
      "#.........###.",
      "..#.#.........",
      "#..#....#..#..",
      "#........#.#..",
      "....###..##.#.",
      "#.#.#....E#...",
      "#.............",
      ".#............",
      "..#...#..#....",
      "...........#..",
      "....#.....#...",
      "#.....#......#",
      ".#....#.##...."
    ]
  },
  {
    "name": "Deep Labyrinth",
    "prompt": "Find stopping points and new angles for your portal shots.",
    "board": [
      "S#......#..#....",
      "...#...#...#....",
      ".#...#..#.#..##.",
      "..........#.....",
      "#.#.....#.......",
      "......#..#.#....",
      "..#..#..#..#...#",
      ".........#..#...",
      "...#.##..#.#....",
      ".....#..#....#..",
      "....##...##...##",
      "....#..#.......#",
      "..E..#...##....#",
      "#...##..#...#...",
      "#.#....#..#.....",
      ".#.#.#.##.##..##"
    ]
  },
  {
    "name": "Find your feet",
    "prompt": "A wall can give you somewhere to stop.",
    "board": [
      "S#.#..#",
      ".....#.",
      "#.##...",
      "....E..",
      "....#..",
      "..#.#..",
      "#....#."
    ]
  },
  {
    "name": "Take the long way",
    "prompt": "Being near the door is only part of the problem.",
    "board": [
      "S..#...",
      "...#...",
      ".......",
      "..##E..",
      "#......",
      ".....##",
      "#....#."
    ]
  },
  {
    "name": "Change direction",
    "prompt": "Which stopping point opens a new route?",
    "board": [
      "S#.....",
      ".....##",
      "...#.#.",
      "..#.E.#",
      ".......",
      ".......",
      "...#..."
    ]
  },
  {
    "name": "A useful detour",
    "prompt": "Make a prediction before each move.",
    "board": [
      "S......",
      ".###.#.",
      "#......",
      "....E#.",
      ".......",
      ".......",
      "..#...."
    ]
  }
];
 if(typeof module!=='undefined'&&module.exports)module.exports=levels;else root.GetOutLevels=levels;
})(globalThis);
