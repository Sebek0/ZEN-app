import React from "react";
import Zen from "../../assets/zen.gif";
const Sidebar = () => {

    const clanmates = [
        {
            id: 1,
            name: "Andones",
            emblem: "https://www.bungie.net/common/destiny2_content/icons/8c22047edb1abda0f611c1808b4ae40a.jpg",
        },
        {
            id:2,
            name: "Filip",
            emblem: "https://www.bungie.net/common/destiny2_content/icons/8c22047edb1abda0f611c1808b4ae40a.jpg",  
        },
        {
            id:3,
            name: "Sebek",
            emblem: "https://www.bungie.net/common/destiny2_content/icons/8c22047edb1abda0f611c1808b4ae40a.jpg",
        },
    ]                                                                        


	return (
		<div className='bg-secondary lg:w-96'>
			<div className=' w-full h-1/6 flex align-middle'>
				<div className='text-gray-500 mx-auto my-auto bg-primary/50 rounded-lg p-3 flex flex-row'>

				<img
					src={Zen}
					alt='Zen'
                    width={50}
                    height={50}
					className='mx-auto my-auto rounded-lg'></img>
				<input className=" ml-5 text-white bg-transparent appearance-none focus:outline-0" placeholder="...?"></input>
                    </div>
			</div>
			<div className=' h-4/6 flex align-middle'>
				<div className='text-gray-500 w-10/12 mx-auto h-full my-auto bg-primary/50 rounded-lg '>
					{clanmates.map((clanmate) => (
						<div
							className='relative p-2'
							key={clanmate.id}>
							<img
								src={clanmate.emblem}
								alt={clanmate.name}
								className='rounded-lg object-cover'></img>

							<div className='text-white text-lg absolute top-1/4 right-1/2 left-20'>
								<p>{clanmate.name}</p>
								<strong className='text-xs absolute top-3/4 text-purple-600 drop-shadow-lg'>
									Reckoner
								</strong>
							</div>
							<p className='text-yellow-600 text-2xl text-bold absolute top-1/4 right-1/4 left-3/4'>
								{" "}
								1337{" "}
							</p>
						</div>
					))}
				</div>
			</div>
			<footer className=' h-1/6 hidden lg:flex align-middle'>
				<div className='text-white w-10/12 mx-auto h-1/4 my-auto bg-primary/50 rounded-lg '>
					<div className='flex text-xs align-baseline'>
						<p className='mx-auto pt-3 flex flex-row'>
							Made by Andones, Filip, Sebek <span className='text-md pl-2'> ❤️</span>
						</p>
					</div>
				</div>
			</footer>
		</div>
	);
};

export default Sidebar;
