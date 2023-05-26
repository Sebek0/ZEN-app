import { useState } from "react";
import Main from "./components/content/Main";
import Sidebar from "./components/nav/Sidebar";
import TimeAgo from "javascript-time-ago";

import en from "javascript-time-ago/locale/en.json";

TimeAgo.addDefaultLocale(en);


function App() {
	const [displayedClanmateId, setDisplayedClanmateId] = useState(0);
	return (
				<div className='h-screen bg-primary font-mono flex flex-col flex-shrink-0 lg:flex-row'>
					<Sidebar setDisplayedClanmateId={setDisplayedClanmateId}></Sidebar>
					{displayedClanmateId !== 0 && <Main displayedClanmateId={displayedClanmateId}></Main>}
				</div>
	);
}

export default App;
