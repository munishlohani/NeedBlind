import Image from "next/image";
import logo from "../assets/docc_logo.png";


const Nav: React.FC = () => {
  return (
    <>
      <div className="w-screen flex justify-start  ">
        <div className=" flex z-20  m-3 items-center gap-3 bg-zinc-200 cursor-pointer hover:bg-purple-600 transition-colors duration-300 backdrop-blur-md w-[70px] h-[70px] rounded-full">
        <Image src={logo} alt="logo" height={70} width={70} className="hover:scale-110 transition-all duration-300" />
        </div>
      </div>
    </>
  );
};

export default Nav;
