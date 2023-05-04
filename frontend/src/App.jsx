import Sidebar from "./components/nav/Sidebar";
import Main from "./components/content/Main";
import { useState } from "react";

  import { QueryClient, QueryClientProvider } from "react-query";
	import { ReactQueryDevtools } from "react-query-devtools";

	const queryClient = new QueryClient({});
function App() {        
	const [displayedClanmateId, setDisplayedClanmateId] = useState(0);                         
	return (
		<QueryClientProvider client={queryClient}>
			<>
				<div className='h-screen w-screen bg-primary font-mono flex flex-col flex-shrink-0 lg:flex-row overflow-y-hidden'>
					<Sidebar setDisplayedClanmateId={setDisplayedClanmateId}></Sidebar>
					<Main displayedClanmateId={displayedClanmateId}></Main>
				</div>
			</>
			<ReactQueryDevtools initialIsOpen={true} />
		</QueryClientProvider>
	);
}

export default App;
