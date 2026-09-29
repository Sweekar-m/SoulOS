type SidebarProps = {
  active: "Chat" | "Tools" | "Memory" | "Settings";
  onSelect: (item: SidebarProps["active"]) => void;
};

const items: SidebarProps["active"][] = ["Chat", "Tools", "Memory", "Settings"];

export function Sidebar({ active, onSelect }: SidebarProps) {
  return (
    <aside className="sidebar">
      <div className="brand">soulOS</div>
      <nav aria-label="Primary navigation">
        {items.map((item) => (
          <button key={item} className={active === item ? "active" : ""} onClick={() => onSelect(item)}>
            {item}
          </button>
        ))}
      </nav>
    </aside>
  );
}
