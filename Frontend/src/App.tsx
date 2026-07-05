import { useEffect } from "react";
import { AppLayout } from "./components/layout/AppLayout";
import { useCurveStore } from "./store/curveStore";
import { ModuleId } from "./types/ecc";
import { AuditAttacksView } from "./views/AuditAttacksView";
import { ECDLPView } from "./views/ECDLPView";
import { FiniteFieldView } from "./views/FiniteFieldView";
import { GroupLawView } from "./views/GroupLawView";
import { LearningPathView } from "./views/LearningPathView";
import { ProtocolsView } from "./views/ProtocolsView";
import { WeierstrassExplorer } from "./views/WeierstrassExplorer";

const modules: Record<ModuleId, JSX.Element> = {
  "learning-path": <LearningPathView />,
  weierstrass: <WeierstrassExplorer />,
  "group-law": <GroupLawView />,
  "finite-fields": <FiniteFieldView />,
  ecdlp: <ECDLPView />,
  protocols: <ProtocolsView />,
  "audit-attacks": <AuditAttacksView />,
};

const moduleIds = Object.keys(modules) as ModuleId[];

function readModuleFromHash(): ModuleId | null {
  const hash = window.location.hash.replace("#", "");
  return moduleIds.includes(hash as ModuleId) ? (hash as ModuleId) : null;
}

export default function App() {
  const activeModule = useCurveStore((state) => state.activeModule);
  const setActiveModule = useCurveStore((state) => state.setActiveModule);

  useEffect(() => {
    const initialModule = readModuleFromHash();
    if (initialModule) setActiveModule(initialModule);

    const handleHashChange = () => {
      const moduleFromHash = readModuleFromHash();
      if (moduleFromHash) setActiveModule(moduleFromHash);
    };

    window.addEventListener("hashchange", handleHashChange);
    return () => window.removeEventListener("hashchange", handleHashChange);
  }, [setActiveModule]);

  useEffect(() => {
    if (window.location.hash !== `#${activeModule}`) {
      window.history.replaceState(null, "", `#${activeModule}`);
    }
  }, [activeModule]);

  return <AppLayout>{modules[activeModule]}</AppLayout>;
}
