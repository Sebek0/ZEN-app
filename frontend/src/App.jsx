import Sidebar from "./components/nav/Sidebar";

function App() {                                 
	return (
		<>
			<div className='h-screen w-screen bg-primary font-mono flex flex-col lg:flex-row'>
        <Sidebar></Sidebar>
				<p className='text-8xl'> HI this is a test of the font </p>
			</div>
		</>
	);
}

export default App;
