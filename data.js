const ALBUMS = [
{id:1,title:'Blood and Fog',ko:'피와 안개',trilogy:'fire',place:'The palace · Hanyang',tag:'A name erased',summary:'A woman dies inside the palace, and her death is recorded as illness. The king who loved her begins to uncover who paid for the poison.',people:['king','yeoni','yunje']},
{id:2,title:'Ink and Embers',ko:'먹과 불씨',trilogy:'fire',place:'Jeju · the market · the mountain',tag:'Writing becomes song',summary:'An exiled scholar keeps writing. A market performer carries his words in songs. A woman who took vows after a family purge prepares to leave her mountain.',people:['yunje','talswe','jeongan']},
{id:3,title:'Ash and Seed',ko:'재와 씨앗',trilogy:'fire',place:'The execution ground · a village',tag:'What the writing leaves behind',summary:'The uprising’s survivors must decide how to live with what happened. Years later, a girl who has never been taught to read finds a page beneath the floorboards.',people:['yunje','talswe','jeongan','buni']},
{id:4,title:'Salt and Waves',ko:'소금과 파도',trilogy:'sea',place:'A southern island',tag:'Four lives meet at sea',summary:'A second exiled scholar, a smuggler, an old fisherman and a diver meet on an island. Beneath the northern shoal, a black ship lies out of sight.',people:['sugyeom','baeswe','gapsu','oki']},
{id:5,title:'Sea and Bones',ko:'바다와 뼈',trilogy:'sea',place:'The storm · the wreck',tag:'Evidence beneath the water',summary:'A storm exposes what the seabed has kept. The diver retrieves a chest containing a ledger of bought testimony, and the scholar begins to understand his exile.',people:['sugyeom','baeswe','gapsu','oki']},
{id:6,title:'Island and Stars',ko:'섬과 별',trilogy:'sea',place:'The voyage north · Songni Mountain',tag:'What to do with the truth',summary:'The ledger can travel to the mainland, but the people carrying it want different futures. Their journey leads back to a woman from the Fire Trilogy.',people:['sugyeom','baeswe','gapsu','oki','jeongan']},
{id:7,title:'Snow and Iron',ko:'눈과 쇠',trilogy:'iron',place:'The harbour · the northern border',tag:'The war arrives',summary:'An invasion interrupts the voyage. The state offers pardons to men it once pursued. A blacksmith turns everyday iron into weapons, and Bun-i goes north to record names.',people:['baeswe','smith','buni']},
{id:8,title:'Iron and Blood',ko:'쇠와 피',trilogy:'iron',place:'The northern front',tag:'Enemies in the same line',summary:'A pardoned smuggler and a king’s soldier now fight side by side. Behind them, Bun-i writes the names of the dying. A sealed order comes from the capital.',people:['baeswe','buni','soldier']},
{id:9,title:'Spring and Rust',ko:'봄과 녹',trilogy:'iron',place:'A frozen field · a kitchen',tag:'What survives the war',summary:'The war is over, but the fields have no seed. A farmer searches the frozen ground. The story follows the surviving paper into a salt jar, through a granddaughter’s questions and into a later age.',people:['buni','soldier','farmer','granddaughter']}
];
const PEOPLE = [
{id:'king',name:'The King',ko:'왕',role:'The sovereign',groups:['fire'],chapters:[1],intro:'Once known as a gentle young king, he loves a woman who holds no recognised rank in his palace. Her death changes the way he rules.',spoiler:'He discovers that the poison came from within his own court and signs decrees in blood. The king who appears in chapter 8 is his descendant.',tracks:['ch1-1','ch1-2','ch1-4']},
{id:'yeoni',name:'Yeon-i',ko:'연이',role:'The woman erased from the records',groups:['fire'],chapters:[1],intro:'A woman inside the palace with no title or rank. Her relationship with the king makes her vulnerable to the people who control the official record.',spoiler:'She is poisoned, her death is recorded as illness and her grave is unmarked. Her erasure sets the larger story in motion.',tracks:[]},
{id:'yunje',name:'Yun-je',ko:'윤제',role:'The scholar of the Fire Trilogy',groups:['fire'],chapters:[1,2,3],intro:'A court scholar sent into exile on Jeju for writing what happened. He keeps writing there, and a performer carries his words back to the mainland.',spoiler:'After the uprising fails, Yun-je is executed. A page of his writing survives beneath a floor and is eventually found by Bun-i.',tracks:['ch2-1','ch3-1']},
{id:'talswe',name:'TALSWE',ko:'탈쇠',role:'The performer and messenger',groups:['fire'],chapters:[2,3],intro:'A market performer with no family name. He walks the tightrope by day and carries a scholar’s words inside his songs by night. Chapter 0 tells his earlier life.',spoiler:'He survives the failed uprising, abandons his mask and travels south as a storyteller. Before he was a performer, he was a nobleman’s son.',tracks:['ch2-2','ch3-2']},
{id:'jeongan',name:'Jeong-an',ko:'정안',role:'The woman at the mountain temple',groups:['fire','sea'],chapters:[2,3,6],intro:'After a purge destroys her family, she takes Buddhist vows on Songni Mountain. Jeong-an is her religious name; her birth name remains unrevealed.',spoiler:'She leaves the mountain carrying a torch, then returns after the uprising fails. Later, the travellers from the sea bring her the ledger. She remembers the faces behind its names.',tracks:['ch2-3','ch3-3','ch6-3']},
{id:'buni',name:'Bun-i',ko:'분이',role:'The girl who learns to write',groups:['fire','iron'],chapters:[3,7,8,9],intro:'A village girl who has never been taught to read finds a page under the floorboards. She waits at a teacher’s door, determined to learn what it says.',spoiler:'She becomes a teacher, travels to the front to write down the names of dying men, and entrusts the surviving ledger to a soldier.',tracks:['ch3-4','ch7-4','ch8-3','ch8-4','ch9-2']},
{id:'sugyeom',name:'Su-gyeom',ko:'수겸',role:'The scholar of the Sea Trilogy',groups:['sea'],chapters:[4,5,6],intro:'Another scholar in exile, living on a southern island and teaching children to write in the sand. He is a different character from Yun-je.',spoiler:'When the chest is opened, he realises he was sent to the place where the evidence was buried. He reads the salt-damaged ledger and joins the voyage north.',tracks:['ch4-1','ch5-3']},
{id:'baeswe',name:'Bae-swe',ko:'배쇠',role:'The smuggler',groups:['sea','iron'],chapters:[4,5,6,7,8],intro:'A man with no surname who has survived by sailing under a black sail and asking no questions about his cargo. Finding the wreck changes that arrangement.',spoiler:'He raises a white sail to take the evidence north, then lowers it when war comes. He joins the front line and eventually stands before the king.',tracks:['ch4-2','ch5-2','ch7-1','ch8-1','ch8-2']},
{id:'gapsu',name:'Gap-su',ko:'갑수',role:'The old fisherman',groups:['sea'],chapters:[4,5,6],intro:'He has spent his life on the same sea. A storm took his elder son, illness his younger son, and his wife died waiting.',spoiler:'During a storm, he asks the sea either to take him or return something. The next day, the wreck becomes visible. He later joins the voyage north.',tracks:['ch4-3','ch5-1','ch6-1']},
{id:'oki',name:'Ok-i',ko:'옥이',role:'The haenyeo · breath-hold diver',groups:['sea'],chapters:[4,5,6],intro:'On land she must lower her head. Underwater her skill decides what she can do. She is the first to see the wreck on the northern shoal.',spoiler:'She brings the chest to the surface. During the voyage to the mainland, she chooses to return to the water, where she has a freedom the land does not give her.',tracks:['ch4-4','ch5-4','ch6-4']},
{id:'smith',name:'The Blacksmith',ko:'대장장이',role:'The one who melts iron',groups:['iron'],chapters:[7],intro:'An unnamed smith at a northern border forge. When war comes, the district’s iron arrives in his yard: chains, cooking pots and a temple bell.',spoiler:'He works alone because the others have gone north. He never follows them to the front; the iron he shapes does.',tracks:['ch7-3']},
{id:'soldier',name:'The Soldier',ko:'병졸',role:'The one nobody asked',groups:['iron'],chapters:[8,9],intro:'A young, unnamed soldier in armour that does not fit. He stands next to Bae-swe at the front. He cannot read.',spoiler:'He receives the ledger from Bun-i, survives the war and buries it in his mother’s kitchen inside a salt jar. Decades later his granddaughter asks where it is.',tracks:['ch8-1','ch9-1','ch9-2','ch9-3']},
{id:'farmer',name:'The Farmer',ko:'농부',role:'The soldier’s father',groups:['iron'],chapters:[9],intro:'Too old to fight, he stays with the field. The family ate its seed grain to survive winter, leaving nothing to plant in spring.',spoiler:'While ploughing the frozen ground, he finds his own son and carries him home.',tracks:['ch9-1']},
{id:'granddaughter',name:'The Granddaughter',ko:'손녀',role:'The one who asks',groups:['iron'],chapters:[9],intro:'Her teacher asks the children to learn about the past from their elders. She goes to her grandfather, who would rather tell her about an ox than the war.',spoiler:'She asks about the buried paper. He says he cannot remember. She does not know where it is, but she keeps telling what she heard.',tracks:['ch9-3']}
];
const TRILOGIES={fire:{name:'The Fire Trilogy',ko:'불의 삼부작',word:'Fire burns',color:'#a33229'},sea:{name:'The Sea Trilogy',ko:'바다 삼부작',word:'Salt preserves',color:'#1f4e79'},iron:{name:'The Iron Trilogy',ko:'쇠 삼부작',word:'Iron remembers',color:'#1d6b5e'}};

const TRACKS = [
  {
    "id": "ch1-1",
    "title": "The King's Path",
    "ko": "왕의 길목",
    "page": "https://joseon-universe.com/en/songs/ch1-1.html",
    "listen": "https://www.youtube.com/watch?v=L5hMmUxuS0M&list=OLAK5uy_k96-qL8mkBo38rQDi15fW2N6bUfKoFDDE"
  },
  {
    "id": "ch1-2",
    "title": "Echoes of the Empty Palace",
    "ko": "빈 궁궐 메아리",
    "page": "https://joseon-universe.com/en/songs/ch1-2.html",
    "listen": "https://www.youtube.com/watch?v=DO04CX9b4zE&list=OLAK5uy_k96-qL8mkBo38rQDi15fW2N6bUfKoFDDE"
  },
  {
    "id": "ch1-3",
    "title": "Ghost Fire",
    "ko": "도깨비불",
    "page": "https://joseon-universe.com/en/songs/ch1-3.html",
    "listen": "https://www.youtube.com/watch?v=ksjVF7-Y63o&list=OLAK5uy_k96-qL8mkBo38rQDi15fW2N6bUfKoFDDE"
  },
  {
    "id": "ch1-4",
    "title": "The Blood Seal",
    "ko": "피의 옥새",
    "page": "https://joseon-universe.com/en/songs/ch1-4.html",
    "listen": "https://www.youtube.com/watch?v=nRsX24Tw1qA&list=OLAK5uy_k96-qL8mkBo38rQDi15fW2N6bUfKoFDDE"
  },
  {
    "id": "ch2-1",
    "title": "A Blade at the Brush Tip",
    "ko": "붓끝에 칼",
    "page": "https://joseon-universe.com/en/songs/ch2-1.html",
    "listen": "https://www.youtube.com/watch?v=JmI8lFvRCc4&list=OLAK5uy_mVKzjWWUsql3RNI09QtIJKOkCVOzqnA_Y"
  },
  {
    "id": "ch2-2",
    "title": "The Market Street",
    "ko": "저잣거리",
    "page": "https://joseon-universe.com/en/songs/ch2-2.html",
    "listen": "https://www.youtube.com/watch?v=HfjJu1IxY2w&list=OLAK5uy_mVKzjWWUsql3RNI09QtIJKOkCVOzqnA_Y"
  },
  {
    "id": "ch2-3",
    "title": "The Woman at the Mountain Temple",
    "ko": "산사의 여인",
    "page": "https://joseon-universe.com/en/songs/ch2-3.html",
    "listen": "https://www.youtube.com/watch?v=IUXxe-l1p54&list=OLAK5uy_mVKzjWWUsql3RNI09QtIJKOkCVOzqnA_Y"
  },
  {
    "id": "ch2-4",
    "title": "The Last Signal Fire",
    "ko": "마지막 봉화",
    "page": "https://joseon-universe.com/en/songs/ch2-4.html",
    "listen": "https://www.youtube.com/watch?v=LkRf-R9krbQ&list=OLAK5uy_mVKzjWWUsql3RNI09QtIJKOkCVOzqnA_Y"
  },
  {
    "id": "ch3-1",
    "title": "The Last Brush",
    "ko": "마지막 붓",
    "page": "https://joseon-universe.com/en/songs/ch3-1.html",
    "listen": "https://www.youtube.com/watch?v=GtzG5MAAvRc&list=OLAK5uy_n6Fggol3x4AQDOZRDUmCkSO3_gpH1m5oI"
  },
  {
    "id": "ch3-2",
    "title": "Shadow on the Road",
    "ko": "길 위의 그림자",
    "page": "https://joseon-universe.com/en/songs/ch3-2.html",
    "listen": "https://www.youtube.com/watch?v=OXn5kNwdySY&list=OLAK5uy_n6Fggol3x4AQDOZRDUmCkSO3_gpH1m5oI"
  },
  {
    "id": "ch3-3",
    "title": "The Empty Mountain",
    "ko": "빈 산",
    "page": "https://joseon-universe.com/en/songs/ch3-3.html",
    "listen": "https://www.youtube.com/watch?v=aSQrVlY3YHU&list=OLAK5uy_n6Fggol3x4AQDOZRDUmCkSO3_gpH1m5oI"
  },
  {
    "id": "ch3-4",
    "title": "The First Sprout",
    "ko": "첫 번째 새싹",
    "page": "https://joseon-universe.com/en/songs/ch3-4.html",
    "listen": "https://www.youtube.com/watch?v=H6uNdlKh6BY&list=OLAK5uy_n6Fggol3x4AQDOZRDUmCkSO3_gpH1m5oI"
  },
  {
    "id": "ch4-1",
    "title": "Road of Exile · The Scholar",
    "ko": "유배길",
    "page": "https://joseon-universe.com/en/songs/ch4-1.html",
    "listen": "https://www.youtube.com/watch?v=Ce7peJdmi0E&list=OLAK5uy_kI-PsuI9Xs2Nb_6ll_0zegySXELkC7Lo0"
  },
  {
    "id": "ch4-2",
    "title": "Black Sail · The Smuggler",
    "ko": "검은 돛",
    "page": "https://joseon-universe.com/en/songs/ch4-2.html",
    "listen": "https://www.youtube.com/watch?v=7GizF-1JOSA&list=OLAK5uy_kI-PsuI9Xs2Nb_6ll_0zegySXELkC7Lo0"
  },
  {
    "id": "ch4-3",
    "title": "Old Net · The Old Fisherman",
    "ko": "늙은 그물",
    "page": "https://joseon-universe.com/en/songs/ch4-3.html",
    "listen": "https://www.youtube.com/watch?v=QAAHnS5OfyM&list=OLAK5uy_kI-PsuI9Xs2Nb_6ll_0zegySXELkC7Lo0"
  },
  {
    "id": "ch4-4",
    "title": "Sumbisori · The Haenyeo",
    "ko": "숨비소리",
    "page": "https://joseon-universe.com/en/songs/ch4-4.html",
    "listen": "https://www.youtube.com/watch?v=gAUL1Vz3Xjc&list=OLAK5uy_kI-PsuI9Xs2Nb_6ll_0zegySXELkC7Lo0"
  },
  {
    "id": "ch5-1",
    "title": "The Storm",
    "ko": "폭풍",
    "page": "https://joseon-universe.com/en/songs/ch5-1.html",
    "listen": "https://www.youtube.com/watch?v=SZI8c_YT8QU&list=OLAK5uy_nDTKZX8h0BfLqZju6WeqByfreU6tUuMt8"
  },
  {
    "id": "ch5-2",
    "title": "The Sunken Ship",
    "ko": "가라앉은 배",
    "page": "https://joseon-universe.com/en/songs/ch5-2.html",
    "listen": "https://www.youtube.com/watch?v=4LsXdlR9A7k&list=OLAK5uy_nDTKZX8h0BfLqZju6WeqByfreU6tUuMt8"
  },
  {
    "id": "ch5-3",
    "title": "Salt Letter",
    "ko": "소금 편지",
    "page": "https://joseon-universe.com/en/songs/ch5-3.html",
    "listen": "https://www.youtube.com/watch?v=olyQGex7Tg0&list=OLAK5uy_nDTKZX8h0BfLqZju6WeqByfreU6tUuMt8"
  },
  {
    "id": "ch5-4",
    "title": "Beneath the Water",
    "ko": "물 아래",
    "page": "https://joseon-universe.com/en/songs/ch5-4.html",
    "listen": "https://www.youtube.com/watch?v=ILQR5eKrC5c&list=OLAK5uy_nDTKZX8h0BfLqZju6WeqByfreU6tUuMt8"
  },
  {
    "id": "ch6-1",
    "title": "Big Dipper",
    "ko": "북두칠성",
    "page": "https://joseon-universe.com/en/songs/ch6-1.html",
    "listen": "https://www.youtube.com/watch?v=v012IvsJ-cM&list=OLAK5uy_mZAd_HXoTZM997C7QmGTQGUI__DNRHyp8"
  },
  {
    "id": "ch6-2",
    "title": "The Woman Who Returned to the Water",
    "ko": "물로 돌아간 여자",
    "page": "https://joseon-universe.com/en/songs/ch6-2.html",
    "listen": "https://www.youtube.com/watch?v=rFaetCl7FJc&list=OLAK5uy_mZAd_HXoTZM997C7QmGTQGUI__DNRHyp8"
  },
  {
    "id": "ch6-3",
    "title": "At the Temple Gate",
    "ko": "산문 앞에서",
    "page": "https://joseon-universe.com/en/songs/ch6-3.html",
    "listen": "https://www.youtube.com/watch?v=btfertkmiBM&list=OLAK5uy_mZAd_HXoTZM997C7QmGTQGUI__DNRHyp8"
  },
  {
    "id": "ch6-4",
    "title": "Ieodo",
    "ko": "이어도",
    "page": "https://joseon-universe.com/en/songs/ch6-4.html",
    "listen": "https://www.youtube.com/watch?v=_7jJwnOT4gM&list=OLAK5uy_mZAd_HXoTZM997C7QmGTQGUI__DNRHyp8"
  },
  {
    "id": "ch7-1",
    "title": "Lowering the Sail",
    "ko": "돛을 내리다",
    "page": "https://joseon-universe.com/en/songs/ch7-1.html",
    "listen": "https://www.youtube.com/watch?v=a97cRqo7C_U&list=OLAK5uy_k2dCivhSXRN7BwkoBLmyV_d2NxP3ukFuk"
  },
  {
    "id": "ch7-2",
    "title": "Gather",
    "ko": "모여라",
    "page": "https://joseon-universe.com/en/songs/ch7-2.html",
    "listen": "https://www.youtube.com/watch?v=5niRyFjX3lM&list=OLAK5uy_k2dCivhSXRN7BwkoBLmyV_d2NxP3ukFuk"
  },
  {
    "id": "ch7-3",
    "title": "The Anvil",
    "ko": "모루",
    "page": "https://joseon-universe.com/en/songs/ch7-3.html",
    "listen": "https://www.youtube.com/watch?v=NLAF9_rgldc&list=OLAK5uy_k2dCivhSXRN7BwkoBLmyV_d2NxP3ukFuk"
  },
  {
    "id": "ch7-4",
    "title": "The Empty Line",
    "ko": "빈 줄",
    "page": "https://joseon-universe.com/en/songs/ch7-4.html",
    "listen": "https://www.youtube.com/watch?v=s3cCtMI-gLg&list=OLAK5uy_k2dCivhSXRN7BwkoBLmyV_d2NxP3ukFuk"
  },
  {
    "id": "ch8-1",
    "title": "The First Line",
    "ko": "첫 줄",
    "page": "https://joseon-universe.com/en/songs/ch8-1.html",
    "listen": "https://www.youtube.com/watch?v=-ff4TgcfdQM&list=OLAK5uy_mxu8I4xZWb3hweYUKr1-J4W7fg8IOLVvU"
  },
  {
    "id": "ch8-2",
    "title": "Two Steps",
    "ko": "두 걸음",
    "page": "https://joseon-universe.com/en/songs/ch8-2.html",
    "listen": "https://www.youtube.com/watch?v=mMpUBhC_GVw&list=OLAK5uy_mxu8I4xZWb3hweYUKr1-J4W7fg8IOLVvU"
  },
  {
    "id": "ch8-3",
    "title": "I Listen for the Name",
    "ko": "이름을 듣소",
    "page": "https://joseon-universe.com/en/songs/ch8-3.html",
    "listen": "https://www.youtube.com/watch?v=7KT4UTQRde8&list=OLAK5uy_mxu8I4xZWb3hweYUKr1-J4W7fg8IOLVvU"
  },
  {
    "id": "ch8-4",
    "title": "The Seal",
    "ko": "봉인",
    "page": "https://joseon-universe.com/en/songs/ch8-4.html",
    "listen": "https://www.youtube.com/watch?v=e8VM_WlSLb4&list=OLAK5uy_mxu8I4xZWb3hweYUKr1-J4W7fg8IOLVvU"
  },
  {
    "id": "ch9-1",
    "title": "Frozen Field",
    "ko": "언 밭",
    "page": "https://joseon-universe.com/en/songs/ch9-1.html",
    "listen": "https://www.youtube.com/watch?v=8L8BkYHP534&list=OLAK5uy_kdbasRvKLSIl3DIbZgOpf9XBS04c7cAw8"
  },
  {
    "id": "ch9-2",
    "title": "The Salt Jar",
    "ko": "소금 항아리",
    "page": "https://joseon-universe.com/en/songs/ch9-2.html",
    "listen": "https://www.youtube.com/watch?v=Y-XEx90K9Qw&list=OLAK5uy_kdbasRvKLSIl3DIbZgOpf9XBS04c7cAw8"
  },
  {
    "id": "ch9-3",
    "title": "My Grandfather, See",
    "ko": "우리 할아버지가요",
    "page": "https://joseon-universe.com/en/songs/ch9-3.html",
    "listen": "https://www.youtube.com/watch?v=328P4MBalh4&list=OLAK5uy_kdbasRvKLSIl3DIbZgOpf9XBS04c7cAw8"
  },
  {
    "id": "ch9-4",
    "title": "The Seal — Five Hundred Years Later",
    "ko": "봉인 · 오백 년 뒤",
    "page": "https://joseon-universe.com/en/songs/ch9-4.html",
    "listen": "https://www.youtube.com/watch?v=sbXJi4LcjYI&list=OLAK5uy_kdbasRvKLSIl3DIbZgOpf9XBS04c7cAw8"
  },
  {
    "id": "ch0-1",
    "title": "In Its Place",
    "ko": "제자리",
    "page": "https://joseon-universe.com/en/songs/ch0-1.html",
    "listen": null
  },
  {
    "id": "ch0-2",
    "title": "The Same Sentence",
    "ko": "같은 문장",
    "page": "https://joseon-universe.com/en/songs/ch0-2.html",
    "listen": null
  },
  {
    "id": "ch0-3",
    "title": "Son of a Traitor",
    "ko": "역적의 아들",
    "page": "https://joseon-universe.com/en/songs/ch0-3.html",
    "listen": null
  },
  {
    "id": "ch0-4",
    "title": "Talswe",
    "ko": "탈쇠",
    "page": "https://joseon-universe.com/en/songs/ch0-4.html",
    "listen": null
  },
  {
    "id": "hp-1",
    "title": "Mask Dance",
    "ko": "탈춤",
    "page": "https://joseon-universe.com/en/songs/hp-1.html",
    "listen": "https://www.youtube.com/watch?v=Czjxq-Fzz2c&list=OLAK5uy_kCUwmP0ehX0JsnBSS2NYaS9mweOY8X_Rk"
  },
  {
    "id": "hp-2",
    "title": "Come Down",
    "ko": "내려와라",
    "page": "https://joseon-universe.com/en/songs/hp-2.html",
    "listen": "https://www.youtube.com/watch?v=EbBngaLoDqU&list=OLAK5uy_kCUwmP0ehX0JsnBSS2NYaS9mweOY8X_Rk"
  },
  {
    "id": "hp-3",
    "title": "Night Patrol",
    "ko": "순라",
    "page": "https://joseon-universe.com/en/songs/hp-3.html",
    "listen": "https://www.youtube.com/watch?v=jV0X_jVxk1c&list=OLAK5uy_kCUwmP0ehX0JsnBSS2NYaS9mweOY8X_Rk"
  },
  {
    "id": "hp-4",
    "title": "Ssireum",
    "ko": "씨름",
    "page": "https://joseon-universe.com/en/songs/hp-4.html",
    "listen": "https://www.youtube.com/watch?v=KDGjIemjgss&list=OLAK5uy_kCUwmP0ehX0JsnBSS2NYaS9mweOY8X_Rk"
  },
  {
    "id": "hp-5",
    "title": "Ganggangsullae",
    "ko": "강강술래",
    "page": "https://joseon-universe.com/en/songs/hp-5.html",
    "listen": "https://www.youtube.com/watch?v=lEbPNNx8rxs&list=OLAK5uy_kCUwmP0ehX0JsnBSS2NYaS9mweOY8X_Rk"
  },
  {
    "id": "hp-6",
    "title": "Heaven Cheon, Earth Ji",
    "ko": "하늘 천 땅 지",
    "page": "https://joseon-universe.com/en/songs/hp-6.html",
    "listen": "https://www.youtube.com/watch?v=IwJcg4MACIk&list=OLAK5uy_kCUwmP0ehX0JsnBSS2NYaS9mweOY8X_Rk"
  },
  {
    "id": "hp-7",
    "title": "One More Cup",
    "ko": "한 잔 먹세",
    "page": "https://joseon-universe.com/en/songs/hp-7.html",
    "listen": "https://www.youtube.com/watch?v=WCLWB6z6FE4&list=OLAK5uy_kCUwmP0ehX0JsnBSS2NYaS9mweOY8X_Rk"
  },
  {
    "id": "hp-8",
    "title": "Mapae",
    "ko": "마패",
    "page": "https://joseon-universe.com/en/songs/hp-8.html",
    "listen": "https://www.youtube.com/watch?v=LTvQ8D78YaI&list=OLAK5uy_kCUwmP0ehX0JsnBSS2NYaS9mweOY8X_Rk"
  }
];

TRACKS.find(t => t.id === 'ch0-4').title = 'TALSWE';

// Original SoundCloud players for the origin EP.
Object.assign(TRACKS.find(t=>t.id==='ch0-1'),{"listen":"https://soundcloud.com/demosaii/in-its-place","embed":"https://w.soundcloud.com/player/?url=https%3A%2F%2Fsoundcloud.com%2Fdemosaii%2Fin-its-place&color=%238c2f2a&auto_play=false&hide_related=true&show_comments=false&show_user=true&show_reposts=false&show_teaser=false"});
Object.assign(TRACKS.find(t=>t.id==='ch0-2'),{"listen":"https://soundcloud.com/demosaii/the-same-sentence","embed":"https://w.soundcloud.com/player/?url=https%3A%2F%2Fsoundcloud.com%2Fdemosaii%2Fthe-same-sentence&color=%238c2f2a&auto_play=false&hide_related=true&show_comments=false&show_user=true&show_reposts=false&show_teaser=false"});
Object.assign(TRACKS.find(t=>t.id==='ch0-3'),{"listen":"https://soundcloud.com/demosaii/son-of-a-traitor","embed":"https://w.soundcloud.com/player/?url=https%3A%2F%2Fsoundcloud.com%2Fdemosaii%2Fson-of-a-traitor&color=%238c2f2a&auto_play=false&hide_related=true&show_comments=false&show_user=true&show_reposts=false&show_teaser=false"});
Object.assign(TRACKS.find(t=>t.id==='ch0-4'),{"listen":"https://soundcloud.com/demosaii/talswe","embed":"https://w.soundcloud.com/player/?url=https%3A%2F%2Fsoundcloud.com%2Fdemosaii%2Ftalswe&color=%238c2f2a&auto_play=false&hide_related=true&show_comments=false&show_user=true&show_reposts=false&show_teaser=false"});
